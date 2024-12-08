/**
 * Copyright 2024 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_ATTN_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_ATTN_H_

#include <fstream>
#include <iostream>
#include <limits>
#include <string>
#include <vector>

#include "acl/acl.h"
#include "aclnnop/aclnn_incre_flash_attention_v3.h"
#include "aclnnop/aclnn_prompt_flash_attention_v3.h"
#include "aclnnop/aclnn_flash_attention_score.h"

#include "acme/src/ops/llama/quant.h"
#include "acme/src/ops/llama/butils.h"
#include "acme/src/ops/llama/gemm.h"
#include "acme/src/ops/llama/comm_adapter.h"
#include "acme/src/ops/llama/kernel/encoder_vector_kernels.h"
#include "acme/src/ops/llama/kernel/tiling_data.h"
#include "utils/log/log.h"
#include "acme/src/core/kernel_loader/so_kernel_loader.h"

namespace mindspore::acme {

template <typename T>
class FlashAttn {
  typedef struct {
    uint64_t workspace_size_ = 0;
    aclTensor *q_ = nullptr;
    aclTensor *k_ = nullptr;
    aclTensor *v_ = nullptr;
    aclTensor *mask_ = nullptr;
    aclTensor *out_ = nullptr;
    int tensor_list_len_ = 0;
    std::vector<aclTensor *> k_arr_;
    std::vector<aclTensor *> v_arr_;
    aclTensorList *k_list_ = nullptr;
    aclTensorList *v_list_ = nullptr;
    aclIntArray *act_seq_ = nullptr;
    aclIntArray *act_seq_q_ = nullptr;
    aclTensor *softmax_max_ = nullptr;
    aclTensor *softmax_sum_ = nullptr;
    aclOpExecutor *executor_ = nullptr;
  } AttnAclExecT;

 public:
  FlashAttn() = default;

  void Prepare(Quant q_w, Quant kv_w, void *qkv_b, void *k_cache, void *v_cache, Quant projection_w, void *projection_b,
               void *sin, void *cos, TransformerParamT *p, int vcores, int ccores) {
    cube_cores_ = ccores;
    vec_cores_ = vcores;
    if (p->is_query_ || p->desc.head_num_ != p->desc.kv_head_num_) {
      q_w_ = q_w;
      kv_w_ = kv_w;
    } else {
      qkv_w_ = q_w;
    }
    k_cache_ = k_cache;
    v_cache_ = v_cache;
    qkv_b_ = qkv_b;
    projection_w_ = projection_w;
    projection_b_ = projection_b;
    if (p->rotary_embedding_) {
      sin_ = sin;
      cos_ = cos;
    }
    act_seq_arr_.resize(p->desc.batch_size_);
    act_seq_arr_q_.resize(p->desc.batch_size_);
    act_seq_arr_inc_.resize(p->desc.batch_size_);
    act_seq_arr_inc_q_.resize(p->desc.batch_size_);

    for (size_t j = 0; j < max_elem_; j++) {
      incremental_[j].k_arr_.resize(p->desc.batch_size_);
      incremental_[j].v_arr_.resize(p->desc.batch_size_);

      incremental_[j].tensor_list_len_ = p->desc.batch_size_;
      for (size_t i = 0; i < p->desc.batch_size_; i++) {
        incremental_[j].k_arr_[i] = nullptr;
        incremental_[j].v_arr_[i] = nullptr;
      }
    }

    size_t actual_hid_size = p->desc.head_num_ * p->desc.head_size_;
    size_t actual_kv_hid_size = p->desc.kv_head_num_ * p->desc.head_size_;
    q_len_ = (size_t)p->desc.batch_size_ * (size_t)p->desc.seq_ * (size_t)actual_hid_size * (size_t)sizeof(T);
    q_len_ = ALIGN(q_len_, ASCEND_BUF_ALIGN);
    kv_len_ = (size_t)p->desc.batch_size_ * (size_t)p->desc.seq_ * (size_t)actual_kv_hid_size * (size_t)sizeof(T);
    kv_len_ = ALIGN(kv_len_, ASCEND_BUF_ALIGN);
  }
  void ComputeModeCnt(TransformerParamT *p) {
    inc_count_ = 0;
    prompt_count_ = 0;
    for (size_t i = 0; i < p->desc.batch_size_; i++) {
      if (p->act_q_seq_[i] == 0) continue;
      if ((p->batch_to_batch_ != nullptr && p->mode_per_batch_[i] > 0) ||
          (p->batch_to_batch_ == nullptr && p->incremental_mode_)) {
        act_seq_arr_inc_q_[inc_count_] = p->act_q_seq_[i];
        act_seq_arr_inc_[inc_count_] = p->act_kv_seq_[i];
        inc_count_++;
      } else {
        act_seq_arr_[prompt_count_] = p->act_kv_seq_[i];
        act_seq_arr_q_[prompt_count_] = p->act_kv_seq_[i];
        prompt_count_++;
      }
    }
  }
  int ComputeDistAttn(void *q, void *k, void *v, void *mask, void *mask_inc, void *block_table, void *act_block_table,
                      TransformerParamT *p, VSLDescT vsl_desc, void *output, void *sys_ws, size_t sys_ws_size,
                      void *stream) {
    size_t q_len = (size_t)p->desc.seq_ * (size_t)p->desc.head_num_ * (size_t)p->desc.head_size_ * (size_t)sizeof(T);
    size_t q_len_inc = (size_t)p->desc.head_num_ * (size_t)p->desc.head_size_ * (size_t)sizeof(T);
    size_t softmax_len = (size_t)p->desc.seq_ * (size_t)p->desc.head_num_ * (size_t)8 * (size_t)sizeof(float);
    size_t softmax_inc_len = (size_t)p->desc.head_num_ * (size_t)8 * (size_t)sizeof(float);
    if (prompt_count_ > 0) {
      prepareAttentionExecuter(q, mask, p, &prompt_, sys_ws_size, output, prompt_count_, false, k, v);
      auto ret = aclnnPromptFlashAttentionV3(sys_ws, prompt_.workspace_size_, prompt_.executor_, stream);
      if (ret != ACL_SUCCESS) {
        MSOP_LOG(ERROR) << "error in aclnnPromptFlashAttention " << ret;
        return ret;
      }
      // copy k, v to remote device
    }
    if (inc_count_ > 0) {
      void *inc_q_start = reinterpret_cast<uint8_t *>(q) + (size_t)prompt_count_ * q_len;
      void *actual_inc_out = reinterpret_cast<uint8_t *>(output) + (size_t)prompt_count_ * q_len;
      void *inc_out_start = actual_inc_out;
      void *softmax_max_start = reinterpret_cast<uint8_t *>(q) + prompt_count_ * q_len + inc_count_ * q_len_inc;
      void *softmax_sum_start =
        reinterpret_cast<uint8_t *>(softmax_max_start) + inc_count_ * softmax_inc_len * dist_size_;
      if (dist_size_ > 1)
        inc_out_start = reinterpret_cast<uint8_t *>(softmax_sum_start) + inc_count_ * softmax_inc_len * dist_size_;
      // iterate over batch element
      for (size_t i = 0; i < inc_count_; i++) {
        void *inc_q = reinterpret_cast<uint8_t *>(inc_q_start) + i * q_len_inc;
        void *inc_out = reinterpret_cast<uint8_t *>(inc_out_start) + i * dist_size_ * q_len_inc;
        softmax_max_ = reinterpret_cast<uint8_t *>(softmax_max_start) + i * softmax_inc_len * dist_size_;
        softmax_sum_ = reinterpret_cast<uint8_t *>(softmax_sum_start) + i * softmax_inc_len * dist_size_;
        // iterate over dist element
        for (size_t j = 0; j < dist_size_; j++) {
          prepareAttentionScoreExecuter(inc_q, mask_inc, p, &incremental_[i * dist_size_ + j], sys_ws_size, inc_out, i,
                                        true, nullptr, nullptr, 0, j, dist_size_);
          auto ret = aclnnFlashAttentionVarLenScore(sys_ws, incremental_[i * dist_size_ + j].workspace_size_,
                                                    incremental_[i * dist_size_ + j].executor_, stream);
          if (ret != ACL_SUCCESS) {
            MSOP_LOG(ERROR) << "error in aclnnIncreFlashAttention " << ret << aclGetRecentErrMsg();
            return ret;
          }
          softmax_max_ = reinterpret_cast<uint8_t *>(softmax_max_) + softmax_inc_len;
          softmax_sum_ = reinterpret_cast<uint8_t *>(softmax_sum_) + softmax_inc_len;
          inc_out = reinterpret_cast<uint8_t *>(inc_out) + q_len_inc;
        }
      }
      void *softmax_max_out = reinterpret_cast<uint8_t *>(inc_out_start) + dist_size_ * inc_count_ * q_len_inc;
      void *softmax_sum_out = reinterpret_cast<uint8_t *>(softmax_max_out) + inc_count_ * softmax_inc_len;

      if (dist_size_ > 1)
        NormalizationDistAttnAscendc(inc_out_start, actual_inc_out, softmax_max_start, softmax_sum_start,
                                     softmax_max_out, softmax_sum_out, vsl_desc, inc_count_, p->desc, dist_size_,
                                     vec_cores_, stream);
    }
    return ACL_SUCCESS;
  }
  int ComputeAttn(void *q, void *k, void *v, void *mask, void *mask_inc, void *block_table, void *act_block_table,
                  TransformerParamT *p, VSLDescT vsl_desc, void *output, void *sys_ws, size_t sys_ws_size,
                  void *stream) {
    // run prompt requests
    if (prompt_count_ > 0) {
      prepareAttentionExecuter(q, mask, p, &prompt_, sys_ws_size, output, prompt_count_, false, k, v);
      auto ret = aclnnPromptFlashAttentionV3(sys_ws, prompt_.workspace_size_, prompt_.executor_, stream);
      if (ret != ACL_SUCCESS) {
        MSOP_LOG(ERROR) << "error in aclnnPromptFlashAttention " << ret;
        return ret;
      }
    }
    // run incremental requests
    if (inc_count_ > 0) {
      size_t q_len = static_cast<size_t>(p->desc.seq_) * static_cast<size_t>(p->desc.head_num_) *
                     static_cast<size_t>(p->desc.head_size_) * sizeof(T);
      void *inc_q = reinterpret_cast<uint8_t *>(q) + static_cast<size_t>(prompt_count_) * q_len;
      void *inc_out = reinterpret_cast<uint8_t *>(output) + static_cast<size_t>(prompt_count_) * q_len;
      prepareAttentionExecuter(inc_q, mask_inc, p, &incremental_[0], sys_ws_size, inc_out, inc_count_, true, nullptr,
                               nullptr, act_block_table);
      auto ret = aclnnIncreFlashAttentionV3(sys_ws, incremental_[0].workspace_size_, incremental_[0].executor_, stream);
      if (ret != ACL_SUCCESS) {
        MSOP_LOG(ERROR) << "error in aclnnIncreFlashAttention " << ret << aclGetRecentErrMsg();
        return ret;
      }
    }
    return ACL_SUCCESS;
  }

  int Compute(void *input, void *mask, void *mask_inc, void *position_idx, void *embedding_table, void *block_table,
              void *act_block_table, void *output, TransformerParamT *p, VSLDescT vsl_desc, void *ws, void *sys_ws,
              size_t sys_ws_size, void *stream) {
    void *qkv_output = ws;
    void *query = reinterpret_cast<uint8_t *>(ws) + q_len_ + 2 * kv_len_;
    void *ws_qkv = query;
    // count number of prompt and number of incremental requests
    ComputeModeCnt(p);
    bool prompt_copy_ = (prompt_count_ > 0) && (p->desc.paged_attention_ || prompt_count_ < p->desc.batch_size_);
    bool b2b_copy_ = (inc_count_ < p->desc.batch_size_ && prompt_count_ < p->desc.batch_size_);

    void *k_prompt = (prompt_copy_) ? reinterpret_cast<uint8_t *>(query) + q_len_ : k_cache_;
    void *v_prompt = (prompt_copy_) ? reinterpret_cast<uint8_t *>(k_prompt) + kv_len_ : v_cache_;
    ComputeQKV(input, position_idx, embedding_table, vsl_desc, qkv_output, ws_qkv, sys_ws, sys_ws_size, p, stream);
    void *batch_to_batch = vsl_desc.batch_to_batch_;
    vsl_desc.batch_to_batch_ = (b2b_copy_) ? batch_to_batch : nullptr;

    QUERY_KERNEL_FUNCTION(qkv_permute, decltype(&QKVPermuteAscendc), "llama", "QKVPermuteAscendc");
    qkv_permute(qkv_output, qkv_b_, query, k_cache_, v_cache_, vsl_desc, (prompt_copy_) ? k_prompt : nullptr,
                (prompt_copy_) ? v_prompt : nullptr, sin_, cos_, block_table, p->token_num_, p->desc, vec_cores_,
                stream);
    vsl_desc.batch_to_batch_ = batch_to_batch;
    // // Compute Attention
    ComputeAttn(query, k_prompt, v_prompt, mask, mask_inc, block_table, act_block_table, p, vsl_desc, ws, sys_ws,
                sys_ws_size, stream);
    void *proj_in = ws;
    // if batch equal to 1, no need to do squeeze
    if (p->desc.batch_size_ > 1 && !p->incremental_mode_) {
      // do squeeze !
      size_t transpose_offset = q_len_;
      proj_in = reinterpret_cast<void *>(reinterpret_cast<uint8_t *>(ws) + transpose_offset);
      QUERY_KERNEL_FUNCTION(squeeze_kernel, decltype(&SqueezeAscendc), "llama", "SqueezeAscendc")
      squeeze_kernel(ws, proj_in, vsl_desc, p->token_num_, p->desc, vec_cores_, stream);
    }

    gemm_projection_.execute(1, p->token_num_, p->desc.hid_dim_, p->desc.head_num_ * p->desc.head_size_, proj_in,
                             &projection_w_, output, sys_ws, sys_ws_size, stream, false, p->w_nz, false);

    if (p->rank_num_ > 1) {
      auto &ccl = CommAdapter::GetInstance();
      uint64_t count = p->token_num_ * p->desc.hid_dim_;
      ccl.AllSumReduce(output, output, count, stream);
    }
    return ACL_SUCCESS;
  }

  size_t GetWsSize(TransformerParamT *p) {
    size_t qkv_len = (1 * q_len_ + 2 * kv_len_);
    size_t len = 0;
    return 2 * qkv_len + len;
  }

  size_t GetSysWsSize(TransformerParamT *p, void *stream) {
    p->token_num_ = p->desc.seq_;
    p->token_num2_ = p->desc.seq_;
    auto ret = prepareAttentionExecuter(nullptr, nullptr, p, &prompt_, 0, nullptr, p->desc.batch_size_, false, nullptr,
                                        nullptr, nullptr, p->desc.seq_);
    if (ret != 0) {
      MSOP_LOG(ERROR) << "prepareAttentionV3Executer  prompt failed.";
      return -1;
    }
    ret = prepareAttentionExecuter(nullptr, nullptr, p, &incremental_[0], 0, nullptr, p->desc.batch_size_, true,
                                   nullptr, nullptr, nullptr, p->desc.seq_ - 1);
    if (ret != 0) {
      MSOP_LOG(ERROR) << "prepareAttentionV3Executer incremental failed.";
      return -1;
    }
    uint64_t qkv_sys_ws = 0;
    size_t actual_hid_size = p->desc.head_num_ * p->desc.head_size_;
    size_t actual_kv_hid_size = p->desc.kv_head_num_ * p->desc.head_size_;
    if (p->is_query_) {
      qkv_sys_ws = std::max(
        gemm_q_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, actual_hid_size, p->desc.hid_dim_, stream, p->w_nz),
        gemm_kv_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, actual_kv_hid_size, p->desc.hid_dim_, stream, false,
                          p->w_nz, false));
    } else if (p->desc.head_num_ == p->desc.kv_head_num_) {
      qkv_sys_ws = gemm_qkv_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, 3 * actual_hid_size, p->desc.hid_dim_,
                                      stream, false, p->w_nz, false);
    } else {
      qkv_sys_ws = std::max(
        gemm_q_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, actual_hid_size, p->desc.hid_dim_, stream, false,
                         p->w_nz, false, p->desc.hid_dim_, actual_hid_size, 2 * actual_kv_hid_size + actual_hid_size),
        gemm_kv_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, 2 * actual_kv_hid_size, p->desc.hid_dim_, stream,
                          false, p->w_nz, false, p->desc.hid_dim_, 2 * actual_kv_hid_size,
                          2 * actual_kv_hid_size + actual_hid_size));
    }
    return std::max({qkv_sys_ws,
                     gemm_projection_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, p->desc.hid_dim_, actual_hid_size,
                                               stream, false, p->w_nz, false),
                     prompt_.workspace_size_, incremental_[0].workspace_size_});
  }

  ~FlashAttn() {
    DestroyExecuter();
    act_seq_arr_.clear();
    act_seq_arr_inc_.clear();
    act_seq_arr_inc_q_.clear();
    act_seq_arr_q_.clear();
  }

 private:
  int ComputeQKV(void *input, void *position_idx, void *embedding_table, VSLDescT vsl_desc, void *qkv_output, void *ws,
                 void *sys_ws, size_t sys_ws_size, TransformerParamT *p, void *stream) {
    void *alt_stream = p->alt_stream_ptr_;
    size_t actual_hid_size = p->desc.head_num_ * p->desc.head_size_;
    size_t actual_kv_hid_size = p->desc.kv_head_num_ * p->desc.head_size_;
    void *query = ws;
    if (p->is_moe_ && !p->incremental_mode_) aclrtSynchronizeStream(alt_stream);
    if (p->is_query_) {
      void *act_stream = p->incremental_mode_ ? stream : alt_stream;
      // step I - multiply KV
      void *kv_out = reinterpret_cast<uint8_t *>(qkv_output) + actual_hid_size * sizeof(T);
      void *ws_kv = reinterpret_cast<uint8_t *>(sys_ws);
      gemm_kv_.execute(1, p->token_num_, 2 * actual_hid_size, p->desc.hid_dim_, input, &kv_w_, kv_out, ws_kv,
                       sys_ws_size, stream, false, p->w_nz, false, nullptr, p->desc.hid_dim_, 2 * actual_hid_size,
                       3 * actual_hid_size);
      // step II - generate q signal from query embedding
      if (!fuse_embed_) {
        fuse_embed_ = true;
        void *temp = reinterpret_cast<uint8_t *>(sys_ws);
        int out_len = p->desc.seq_ * actual_hid_size * sizeof(T);
        void *temp_ws = reinterpret_cast<uint8_t *>(sys_ws) + out_len;
        Gemm gemm;
        gemm.execute(1, p->desc.seq_, actual_hid_size, p->desc.hid_dim_, embedding_table, &q_w_, temp, temp_ws,
                     sys_ws_size, stream, false, p->w_nz, false);
        auto ret = aclrtMemcpyAsync(embedding_table, out_len, temp, out_len, ACL_MEMCPY_DEVICE_TO_DEVICE, stream);
        if (ret != ACL_SUCCESS) {
          MSOP_LOG(ERROR) << "aclrtMemcpyAsync failed.";
          return ret;
        }
        SyncDevice(stream);
      }

      QUERY_KERNEL_FUNCTION(vocab_embedding, decltype(&VocabEmbeddingAscendc), "llama", "VocabEmbeddingAscendc");
      vocab_embedding(position_idx, embedding_table, qkv_output, vsl_desc, p->token_num_, p->desc, vec_cores_,
                      act_stream);
      // step III - Make sure q sig is ready
      if (!p->incremental_mode_) SyncDevice(alt_stream);
    } else if (p->desc.head_num_ == p->desc.kv_head_num_) {
      gemm_qkv_.execute(1, p->token_num_, 3 * actual_hid_size, p->desc.hid_dim_, input, &qkv_w_, qkv_output, sys_ws,
                        sys_ws_size, stream, false, p->w_nz,
                        false);  // fix actual_kv_hid_size for llama
    } else {
      void *kv_out = reinterpret_cast<uint8_t *>(qkv_output) + actual_hid_size * sizeof(T);
      void *ws_kv = reinterpret_cast<uint8_t *>(sys_ws);
      gemm_q_.execute(1, p->token_num_, actual_hid_size, p->desc.hid_dim_, input, &q_w_, qkv_output, sys_ws,
                      sys_ws_size, stream, false, p->w_nz, false, nullptr, p->desc.hid_dim_, actual_hid_size,
                      2 * actual_kv_hid_size + actual_hid_size);  // fix actual_kv_hid_size for llama
      gemm_kv_.execute(1, p->token_num_, 2 * actual_kv_hid_size, p->desc.hid_dim_, input, &kv_w_, kv_out, ws_kv,
                       sys_ws_size, stream, false, p->w_nz, false, nullptr, p->desc.hid_dim_, 2 * actual_kv_hid_size,
                       2 * actual_kv_hid_size + actual_hid_size);
    }
    return ACL_SUCCESS;
  }

  void cleanupExecuter(AttnAclExecT *handle) {
    if (handle->q_) {
      aclDestroyTensor(handle->q_);
      handle->q_ = nullptr;
    }
    if (handle->k_list_) {
      aclDestroyTensorList(handle->k_list_);
      handle->k_list_ = nullptr;
      handle->k_ = nullptr;
      for (size_t i = 0; i < handle->tensor_list_len_; i++) handle->k_arr_[i] = nullptr;  // cleanup in list destroy
    } else {
      if (handle->k_) {
        aclDestroyTensor(handle->k_);
        handle->k_ = nullptr;
      }
    }
    if (handle->v_list_) {
      aclDestroyTensorList(handle->v_list_);
      handle->v_list_ = nullptr;
      handle->v_ = nullptr;  // cleanup in list destroy
    } else {
      if (handle->v_) {
        aclDestroyTensor(handle->v_);
        handle->v_ = nullptr;
        for (size_t i = 0; i < handle->tensor_list_len_; i++) handle->v_arr_[i] = nullptr;  // cleanup in list destroy
      }
    }
    if (handle->mask_) {
      aclDestroyTensor(handle->mask_);
      handle->mask_ = nullptr;
    }
    if (handle->out_) {
      aclDestroyTensor(handle->out_);
      handle->out_ = nullptr;
    }
    if (handle->act_seq_) {
      aclDestroyIntArray(handle->act_seq_);
      handle->act_seq_ = nullptr;
    }
    if (handle->act_seq_q_) {
      aclDestroyIntArray(handle->act_seq_q_);
      handle->act_seq_q_ = nullptr;
    }
    if (handle->softmax_max_) {
      aclDestroyTensor(handle->softmax_max_);
      handle->softmax_max_ = nullptr;
    }
    if (handle->softmax_sum_) {
      aclDestroyTensor(handle->softmax_sum_);
      handle->softmax_sum_ = nullptr;
    }
    handle->executor_ = nullptr;
  }

  int prepareAttentionScoreExecuter(void *query, void *mask, TransformerParamT *p, AttnAclExecT *handle,
                                    size_t sys_ws_size, void *output, int inc_id, bool is_inc, void *k_prompt = nullptr,
                                    void *v_prompt = nullptr, int max_tokens = 0, int dist_id = 0, int dist_size_ = 1) {
    cleanupExecuter(handle);
    int sum_null = 0;
    int inc_count_ = 0;
    int real_batch = inc_id;
    int token_num;
    if (max_tokens != 0) {
      for (size_t i = 0; i < p->desc.batch_size_; i++) {
        act_seq_arr_[i] = max_tokens;
        act_seq_arr_q_[i] = max_tokens;
        token_num = max_tokens;
      }
    } else {
      token_num = p->act_kv_seq_[inc_id];
    }
    if (p->batch_to_batch_ != nullptr && max_tokens == 0) {
      if (is_inc) {
        real_batch = p->batch_to_batch_[prompt_count_ + inc_id];
      }
      token_num = p->act_kv_seq_[prompt_count_ + inc_id];
    }
    int elem_count = token_num / dist_size_;
    int kv_size = elem_count;
    if (dist_id == dist_size_ - 1) kv_size += token_num % dist_size_;
    std::vector<int64_t> q_shape{is_inc ? 1 : p->desc.seq_, p->desc.head_num_, p->desc.head_size_};
    auto q_stride = calcStride(q_shape);

    std::vector<int64_t> kv_shape{kv_size, p->desc.kv_head_num_, p->desc.head_size_};
    auto kv_stride = calcStride(kv_shape);

    std::vector<int64_t> mask_shape{is_inc ? 1 : p->desc.seq_, p->desc.kv_seq_};
    auto mask_stride = calcStride(mask_shape);
    mask_shape = {is_inc ? 1 : p->desc.seq_, kv_size};

    int cur_batch = real_batch * p->desc.kv_seq_ * p->desc.kv_head_num_ * p->desc.head_size_ * sizeof(T);
    void *act_k = (is_inc) ? k_cache_ : k_prompt;
    void *act_v = (is_inc) ? v_cache_ : v_prompt;
    act_k = reinterpret_cast<uint8_t *>(act_k) + cur_batch +
            sizeof(T) * dist_id * elem_count * p->desc.kv_head_num_ * p->desc.head_size_;
    act_v = reinterpret_cast<uint8_t *>(act_v) + cur_batch +
            sizeof(T) * dist_id * elem_count * p->desc.kv_head_num_ * p->desc.head_size_;
    void *act_mask = reinterpret_cast<uint8_t *>(mask) + sizeof(T) * dist_id * elem_count;

    handle->q_ = aclCreateTensor(q_shape.data(), q_shape.size(), aclDataType::ACL_FLOAT16, q_stride.data(), 0,
                                 aclFormat::ACL_FORMAT_ND, q_shape.data(), q_shape.size(), query);
    handle->k_ = aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                                 aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), act_k);
    handle->v_ = aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                                 aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), act_v);
    handle->mask_ = aclCreateTensor(mask_shape.data(), mask_shape.size(), aclDataType::ACL_BOOL, mask_stride.data(), 0,
                                    aclFormat::ACL_FORMAT_ND, mask_shape.data(), mask_shape.size(), act_mask);
    handle->out_ = aclCreateTensor(q_shape.data(), q_shape.size(), aclDataType::ACL_FLOAT16, q_stride.data(), 0,
                                   aclFormat::ACL_FORMAT_ND, q_shape.data(), q_shape.size(), output);

    int64_t act_arr[1]{kv_size};
    int64_t act_q_arr[1]{(is_inc) ? act_seq_arr_inc_q_[inc_id] : act_seq_arr_q_[inc_id]};

    handle->act_seq_ = aclCreateIntArray(act_arr, 1);
    handle->act_seq_q_ = aclCreateIntArray(act_q_arr, 1);
    char format[] = "TND";
    aclnnStatus ret = ACL_SUCCESS;
    std::vector<int64_t> softmax_shape{is_inc ? 1 : p->desc.seq_, p->desc.head_num_, 8};
    auto softmax_stride = calcStride(softmax_shape);
    handle->softmax_max_ =
      aclCreateTensor(softmax_shape.data(), softmax_shape.size(), aclDataType::ACL_FLOAT, softmax_stride.data(), 0,
                      aclFormat::ACL_FORMAT_ND, softmax_shape.data(), softmax_shape.size(), softmax_max_);
    handle->softmax_sum_ =
      aclCreateTensor(softmax_shape.data(), softmax_shape.size(), aclDataType::ACL_FLOAT, softmax_stride.data(), 0,
                      aclFormat::ACL_FORMAT_ND, softmax_shape.data(), softmax_shape.size(), softmax_sum_);

    ret = aclnnFlashAttentionVarLenScoreGetWorkspaceSize(
      handle->q_, handle->k_, handle->v_, nullptr, nullptr, nullptr, handle->mask_, nullptr, handle->act_seq_q_,
      handle->act_seq_, p->desc.scale_, 1, 65536, 65536, p->desc.head_num_, format, 0, 0, handle->softmax_max_,
      handle->softmax_sum_, nullptr, handle->out_, &handle->workspace_size_, &handle->executor_);
    if (max_tokens == 0) {
      if (handle->workspace_size_ > sys_ws_size) {
        MSOP_LOG(ERROR) << "error in flush attention workspace size too big:" << handle->workspace_size_ << " "
                        << sys_ws_size;
        return -1;
      }
    }
    if (ret != ACL_SUCCESS) {
      MSOP_LOG(ERROR) << "error in flush attention workspace size (" << ret << ") " << aclGetRecentErrMsg();
      return ret;
    }
    return ACL_SUCCESS;
  }

  int prepareAttentionExecuter(void *query, void *mask, TransformerParamT *p, AttnAclExecT *handle, size_t sys_ws_size,
                               void *output, int batch_size, bool is_inc, void *k_prompt = nullptr,
                               void *v_prompt = nullptr, void *block_table = nullptr, int max_tokens = 0) {
    cleanupExecuter(handle);
    std::vector<int64_t> q_shape{batch_size, is_inc ? 1 : p->desc.seq_, p->desc.head_num_ * p->desc.head_size_};
    auto q_stride = calcStride(q_shape);

    std::vector<int64_t> kv_shape{batch_size, p->desc.seq_, p->desc.kv_head_num_ * p->desc.head_size_};
    auto kv_stride = calcStride(kv_shape);

    std::vector<int64_t> mask_shape{is_inc ? batch_size : p->desc.seq_, (is_inc && p->desc.paged_attention_)
                                                                          ? p->desc.page_num_ * p->desc.page_size_
                                                                          : p->desc.seq_};
    auto mask_stride = calcStride(mask_shape);

    handle->q_ = aclCreateTensor(q_shape.data(), q_shape.size(), aclDataType::ACL_FLOAT16, q_stride.data(), 0,
                                 aclFormat::ACL_FORMAT_ND, q_shape.data(), q_shape.size(), query);
    handle->mask_ = aclCreateTensor(mask_shape.data(), mask_shape.size(), aclDataType::ACL_INT8, mask_stride.data(), 0,
                                    aclFormat::ACL_FORMAT_ND, mask_shape.data(), mask_shape.size(), mask);
    handle->out_ = aclCreateTensor(q_shape.data(), q_shape.size(), aclDataType::ACL_FLOAT16, q_stride.data(), 0,
                                   aclFormat::ACL_FORMAT_ND, q_shape.data(), q_shape.size(), output);
    if (max_tokens != 0) {
      for (size_t i = 0; i < batch_size; i++) {
        act_seq_arr_[i] = max_tokens;
        act_seq_arr_inc_[i] = max_tokens;
      }
      block_table = p->desc.block_table_;
    }
    handle->act_seq_ = aclCreateIntArray((is_inc) ? act_seq_arr_inc_.data() : act_seq_arr_.data(), batch_size);
    // B Batch, N head_num, D headDim, H head_size=head_num*headDim, S SequnceLength
    char format[] = "BSH";
    aclnnStatus ret = ACL_SUCCESS;
    if (is_inc) {
      aclTensor *bt_tensor = nullptr;
      if (p->desc.paged_attention_) {
        kv_shape = {p->desc.batch_size_, p->desc.seq_, p->desc.kv_head_num_ * p->desc.head_size_};
        kv_stride = calcStride(kv_shape);
        handle->k_ = aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                                     aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), k_cache_);
        handle->v_ = aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                                     aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), v_cache_);
        handle->k_list_ = aclCreateTensorList(&handle->k_, 1);
        handle->v_list_ = aclCreateTensorList(&handle->v_, 1);
        std::vector<int64_t> bt_shape{batch_size, ceil(p->desc.seq_ / p->desc.page_size_)};
        auto bt_stride = calcStride(bt_shape);
        bt_tensor = aclCreateTensor(bt_shape.data(), bt_shape.size(), aclDataType::ACL_INT32, bt_stride.data(), 0,
                                    aclFormat::ACL_FORMAT_ND, bt_shape.data(), bt_shape.size(), block_table);
      } else {
        int sum_null = 0;
        T *act_kcache = reinterpret_cast<T *>(k_cache_);
        T *act_vcache = reinterpret_cast<T *>(v_cache_);
        for (size_t i = 0; i < p->desc.batch_size_; i++) {
          if (max_tokens == 0 && p->act_q_seq_[i] == 0) sum_null++;
        }
        for (size_t i = 0; i < batch_size; i++) {
          int real_batch = i;
          if (max_tokens == 0) {
            if (p->batch_to_batch_ != nullptr) {
              real_batch = p->batch_to_batch_[p->desc.batch_size_ - batch_size - sum_null + i];
            }
            act_kcache =
              reinterpret_cast<T *>(k_cache_) + real_batch * p->desc.seq_ * p->desc.kv_head_num_ * p->desc.head_size_;
            act_vcache =
              reinterpret_cast<T *>(v_cache_) + real_batch * p->desc.seq_ * p->desc.kv_head_num_ * p->desc.head_size_;
          }
          kv_shape = {1, act_seq_arr_inc_[i], p->desc.kv_head_num_ * p->desc.head_size_};
          auto kv_stride = calcStride(kv_shape);

          handle->k_arr_[i] =
            aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                            aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), act_kcache);
          handle->v_arr_[i] =
            aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                            aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), act_vcache);
        }
        handle->k_list_ = aclCreateTensorList(handle->k_arr_.data(), batch_size);
        handle->v_list_ = aclCreateTensorList(handle->v_arr_.data(), batch_size);
      }
      ret = aclnnIncreFlashAttentionV3GetWorkspaceSize(
        handle->q_, handle->k_list_, handle->v_list_, nullptr, handle->mask_, handle->act_seq_, nullptr, nullptr,
        nullptr, nullptr, nullptr, nullptr, nullptr, bt_tensor, p->desc.head_num_, p->desc.scale_, format,
        p->desc.kv_head_num_, p->desc.page_size_, 0, handle->out_, &handle->workspace_size_, &handle->executor_);
    } else {
      handle->k_ = aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                                   aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), k_prompt);
      handle->v_ = aclCreateTensor(kv_shape.data(), kv_shape.size(), aclDataType::ACL_FLOAT16, kv_stride.data(), 0,
                                   aclFormat::ACL_FORMAT_ND, kv_shape.data(), kv_shape.size(), v_prompt);
      ret = aclnnPromptFlashAttentionV3GetWorkspaceSize(
        handle->q_, handle->k_, handle->v_, nullptr, handle->mask_, handle->act_seq_, handle->act_seq_, nullptr,
        nullptr, nullptr, nullptr, nullptr, p->desc.head_num_, p->desc.scale_, std::numeric_limits<int>::max(), 0,
        format, p->desc.kv_head_num_, 0, 0, handle->out_, &handle->workspace_size_, &handle->executor_);
    }
    if (ret != ACL_SUCCESS) {
      std::cerr << __FILE__ << ":" << __LINE__ << " aclError:" << ret << " " << aclGetRecentErrMsg() << std::endl;
      return ret;
    }
    if (max_tokens == 0) {
      if (handle->workspace_size_ > sys_ws_size) {
        MSOP_LOG(ERROR) << "error in flush attention workspace size too big:" << handle->workspace_size_ << " "
                        << sys_ws_size;
        return -1;
      }
    }
    return ACL_SUCCESS;
  }

  void DestroyExecuter() {
    cleanupExecuter(&prompt_);
    for (size_t i = 0; i < max_elem_; i++) {
      cleanupExecuter(&incremental_[i]);
      incremental_[i].k_arr_.clear();
      incremental_[i].v_arr_.clear();
    }
  }

  int cube_cores_;
  int vec_cores_;
  Gemm gemm_projection_;
#ifdef MATMUL_REDUCE
  GemmDistribute gemmd_projection_;
#endif
  Gemm gemm_q_;
  Gemm gemm_kv_;
  Gemm gemm_qkv_;
  Quant qkv_w_;
  void *qkv_b_ = nullptr;
  Quant q_w_;
  Quant kv_w_;
  void *k_cache_ = nullptr;
  void *v_cache_ = nullptr;
  Quant projection_w_;
  void *softmax_max_ = nullptr;
  void *softmax_sum_ = nullptr;
  void *projection_b_ = nullptr;
  std::vector<int64_t> act_seq_arr_;
  std::vector<int64_t> act_seq_arr_q_;
  std::vector<int64_t> act_seq_arr_inc_;
  std::vector<int64_t> act_seq_arr_inc_q_;
  void *sin_ = nullptr;
  void *cos_ = nullptr;
  void *swap_mask_ = nullptr;
  const int dist_size_ = 2;
  int inc_count_ = 0;
  int prompt_count_ = 0;
  AttnAclExecT prompt_;
  const static int max_elem_ = 2 * 16;
  AttnAclExecT incremental_[max_elem_];
  bool fuse_embed_ = false;
  size_t q_len_, kv_len_;
  bool quant_ = false;
};
}  // namespace mindspore::acme
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_ATTN_H_
