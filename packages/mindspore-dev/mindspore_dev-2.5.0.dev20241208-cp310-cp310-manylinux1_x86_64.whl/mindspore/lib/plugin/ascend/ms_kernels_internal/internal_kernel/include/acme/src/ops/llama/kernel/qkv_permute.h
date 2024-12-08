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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_QKV_PERMUTE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_QKV_PERMUTE_H_

#include "kernel_operator.h"
#include "kernel_utils.h"
#include "tiling_data.h"

using AscendC::GetBlockIdx;
using AscendC::GetBlockNum;
using AscendC::GlobalTensor;
using AscendC::LocalTensor;
using AscendC::QuePosition;
using AscendC::TBuf;
using AscendC::TPipe;
using AscendC::TQue;

template <typename T, int PipeSize>
class KernelPermuteQKV {
 public:
  __aicore__ inline KernelPermuteQKV() = default;
  __aicore__ inline void Init(GM_ADDR qkv_ptr, GM_ADDR bias_ptr, GM_ADDR q_ptr, GM_ADDR k_cache_ptr,
                              GM_ADDR v_cache_ptr, VSLDescDT vsl_desc, GM_ADDR k_prompt, GM_ADDR v_prompt,
                              GM_ADDR sin_ptr, GM_ADDR cos_ptr, GM_ADDR block_table, int actual_token,
                              TransformerDescT desc_p, int total_blocks, int per_core_blocks) {
    // initialize VSL
    vsl_helper_.Init(vsl_desc.act_q_seq_, vsl_desc.act_kv_seq_, vsl_desc.q_padding_, vsl_desc.kv_padding_,
                     vsl_desc.mode_per_batch_, actual_token, desc_p.batch_size_, desc_p.seq_, &pipe_);
    int D = desc_p.head_num_ * desc_p.head_size_;
    int kv_D = desc_p.kv_head_num_ * desc_p.head_size_;
    head_size_ = desc_p.head_size_;
    head_num_ = desc_p.head_num_;
    kv_head_num_ = desc_p.kv_head_num_;
    max_seq_len_ = desc_p.seq_;
    batch_ = desc_p.batch_size_;
    actual_token_ = actual_token;
    total_blocks_ = total_blocks;
    per_core_blocks_ = per_core_blocks;
    block_size_ = desc_p.page_size_;
    num_blocks_ = desc_p.page_num_;
    block_tbl_dim_ = UP_DIV(max_seq_len_, block_size_);
    paged_attention_ = desc_p.paged_attention_;
    constexpr int EmbeddingFactor = 3;
    qkv_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(qkv_ptr),
                                actual_token_ * (kv_D * (EmbeddingFactor - 1) + D));
    q_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(q_ptr), actual_token_ * D);
    if (paged_attention_) {
      k_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(k_cache_ptr), num_blocks_ * block_size_ * kv_D);
      v_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(v_cache_ptr), num_blocks_ * block_size_ * kv_D);
      block_table_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(block_table), block_tbl_dim_ * batch_);
    } else {
      k_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(k_cache_ptr), batch_ * max_seq_len_ * kv_D);
      v_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(v_cache_ptr), batch_ * max_seq_len_ * kv_D);
    }
    is_batch_2_batch_ = (vsl_desc.batch_to_batch_ != nullptr);
    is_prompt_cpy_ = false;
    if (k_prompt && v_prompt) {
      is_prompt_cpy_ = true;
      k_prompt_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(k_prompt), batch_ * max_seq_len_ * kv_D);
      v_prompt_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(v_prompt), batch_ * max_seq_len_ * kv_D);
    }
    if (is_batch_2_batch_) {
      batch_to_batch_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(vsl_desc.batch_to_batch_), batch_);
    }

    int head_align_size = ALIGN32(sizeof(T) * (D + 2 * kv_D));
    copy_size_ = head_align_size / sizeof(T);
    pipe_.InitBuffer(in_, PipeSize, head_align_size);
    pipe_.InitBuffer(out_, PipeSize, head_align_size);
    is_bias_ = false;
    if (bias_ptr) {
      is_bias_ = true;
      bias_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(bias_ptr), (EmbeddingFactor - 1) * kv_D + D);
      pipe_.InitBuffer(bias_tmp_buf_, ALIGN32(sizeof(T) * ((EmbeddingFactor - 1) * kv_D + D)));
      bias_local_ = bias_tmp_buf_.Get<T>();
      DataCopy(bias_local_, bias_global_, ALIGN((EmbeddingFactor - 1) * kv_D + D, 16));
      pipe_barrier(PIPE_ALL);
    }
    is_apply_rotary_ = false;
    if (sin_ptr) {
      sin_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(sin_ptr), head_size_ * max_seq_len_);
      pipe_.InitBuffer(sin_tmp_buf_, ALIGN32(sizeof(T) * head_size_));
      sin_local_ = sin_tmp_buf_.Get<T>();
      cos_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(cos_ptr), head_size_ * max_seq_len_);
      pipe_.InitBuffer(cos_tmp_buf_, ALIGN32(sizeof(T) * head_size_));
      cos_local_ = sin_local_[head_size_];
      is_apply_rotary_ = true;
    }
  }
  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    int stride_q = head_num_ * head_size_;
    int stride_kv = kv_head_num_ * head_size_;
    int stride = stride_q + 2 * stride_kv;

    for (size_t i = 0; i < per_core_blocks_; i++) {
      int elem_id = block_id * per_core_blocks_ + i;
      int token_id = elem_id;
      if (elem_id >= total_blocks_) break;
      int batch_id;
      bool incremental;
      vsl_helper_.GetBatchId(token_id, &batch_id);
      vsl_helper_.GetIncrementalMode(batch_id, &incremental);
      int src_offset = token_id * stride;
      if (is_apply_rotary_) {
        copyInSinCos(token_id);
      }
      copyIn(src_offset, copy_size_);
      ProcessQKV();
      CopyOut(token_id, incremental);
    }
  }

  __aicore__ inline void apply_rotary_embedding(LocalTensor<T> &dstLocal, LocalTensor<T> &srcLocal, int head_num) {
    int head_stride = head_size_;
    int mid = head_size_ / 2;
    int stride_q = head_num_ * head_size_;

    LocalTensor<T> qSrcLocal = srcLocal[0];
    LocalTensor<T> kSrcLocal = srcLocal[stride_q];
    LocalTensor<T> qDstLocal = dstLocal[0];
    LocalTensor<T> kDstLocal = dstLocal[stride_q];

    for (size_t i = 0; i < head_num; i++) {
      LocalTensor<T> q_head_in = qSrcLocal[i * head_stride];
      LocalTensor<T> q_head_out = qDstLocal[i * head_stride];
      Adds(q_head_out, q_head_in[mid], (T)0.0f,
           mid);  // copy index [0, 1, ... d/2-1] into [d/2, d/2+1, ... d-1]
      Adds(q_head_out[mid], q_head_in, (T)0.0f, mid);

      LocalTensor<T> k_head_in = kSrcLocal[i * head_stride];
      LocalTensor<T> k_head_out = kDstLocal[i * head_stride];
      Adds(k_head_out, k_head_in[mid], (T)0.0f,
           mid);  // copy index [0, 1, ... d/2-1] into [d/2, d/2+1, ... d-1]
      Adds(k_head_out[mid], k_head_in, (T)0.0f, mid);

      pipe_barrier(PIPE_V);

      Mul(q_head_in, q_head_in, cos_local_, head_stride);
      Mul(q_head_out, q_head_out, sin_local_, head_stride);
      Mul(k_head_in, k_head_in, cos_local_, head_stride);
      Mul(k_head_out, k_head_out, sin_local_, head_stride);

      pipe_barrier(PIPE_V);

      Add(q_head_out, q_head_in, q_head_out, head_stride);
      Add(k_head_out, k_head_in, k_head_out, head_stride);
    }
  }

  __aicore__ inline void apply_rotary_embedding_q(LocalTensor<T> &dstLocal, LocalTensor<T> &srcLocal, int head_num) {
    int head_stride = head_size_;
    int mid = head_size_ / 2;
    int stride_q = head_num_ * head_size_;

    LocalTensor<T> qSrcLocal = srcLocal[0];
    LocalTensor<T> qDstLocal = dstLocal[0];

    for (size_t i = 0; i < head_num; i++) {
      LocalTensor<T> q_head_in = qSrcLocal[i * head_stride];
      LocalTensor<T> q_head_out = qDstLocal[i * head_stride];
      Adds(q_head_out, q_head_in[mid], (T)0.0f,
           mid);  // copy index [0, 1, ... d/2-1] into [d/2, d/2+1, ... d-1]
      Adds(q_head_out[mid], q_head_in, (T)0.0f, mid);
      pipe_barrier(PIPE_V);
      Mul(q_head_in, q_head_in, cos_local_, head_stride);
      Mul(q_head_out, q_head_out, sin_local_, head_stride);
      pipe_barrier(PIPE_V);
      Add(q_head_out, q_head_in, q_head_out, head_stride);
    }
  }

 private:
  __aicore__ inline void copyIn(int offset, int copy_size) {
    LocalTensor<T> srcLocal = in_.template AllocTensor<T>();
    DataCopy(srcLocal, qkv_global_[offset], copy_size);
    in_.EnQue(srcLocal);
  }

  __aicore__ inline void copyInSinCos(int token_id) {
    int position_id;
    vsl_helper_.GetPositionIdByTokenId(token_id, &position_id);
    DataCopy(sin_local_, sin_global_[position_id * head_size_], head_size_);
    DataCopy(cos_local_, cos_global_[position_id * head_size_], head_size_);
    set_flag(PIPE_MTE2, PIPE_V, EVENT_ID3);
    wait_flag(PIPE_MTE2, PIPE_V, EVENT_ID3);
  }

  __aicore__ inline void ProcessQKV() {
    int stride_q = head_num_ * head_size_;
    int stride_kv = kv_head_num_ * head_size_;
    LocalTensor<T> srcLocal = in_.template DeQue<T>();
    LocalTensor<T> qLocal = srcLocal[0];
    LocalTensor<T> kLocal = srcLocal[stride_q];
    LocalTensor<T> vLocal = srcLocal[stride_q + stride_kv];

    LocalTensor<T> dstLocal = out_.template AllocTensor<T>();
    LocalTensor<T> vDstLocal = dstLocal[stride_q + stride_kv];

    int min_head = kv_head_num_ < head_num_ ? kv_head_num_ : head_num_;
    if (is_bias_ && is_apply_rotary_) {
      Add(srcLocal, srcLocal, bias_local_, stride_q + 2 * stride_kv);
      apply_rotary_embedding(dstLocal, srcLocal, min_head);
      if (kv_head_num_ < head_num_) {
        LocalTensor<T> q = qLocal[stride_kv];
        LocalTensor<T> d = dstLocal[stride_kv];
        apply_rotary_embedding_q(q, d, (head_num_ - kv_head_num_));
      }
    } else if (is_bias_ && !is_apply_rotary_) {
      Add(dstLocal, srcLocal, bias_local_, stride_q + 2 * stride_kv);
    } else if (!is_bias_ && is_apply_rotary_) {
      Adds(vDstLocal, vLocal, (T)0.0f, stride_kv);
      apply_rotary_embedding(dstLocal, srcLocal, min_head);
      if (kv_head_num_ < head_num_) {
        LocalTensor<T> q = qLocal[stride_kv];
        LocalTensor<T> d = dstLocal[stride_kv];
        apply_rotary_embedding_q(q, d, (head_num_ - kv_head_num_));
      }
    } else {
      Adds(dstLocal, srcLocal, (T)0.0f, stride_q + 2 * stride_kv);
    }
    out_.EnQue(dstLocal);
    in_.FreeTensor(srcLocal);
  }

  __aicore__ inline void CopyOut(int token_id, int incremental) {
    int stride_q = head_num_ * head_size_;
    int stride_kv = kv_head_num_ * head_size_;
    int q_dst_offset = 0;
    int kv_dst_offset = 0;
    int actual_dst_offset = 0;

    GetQOffset(token_id, &q_dst_offset);
    GetKVOffset(token_id, incremental, &kv_dst_offset, &actual_dst_offset);
    LocalTensor<T> dstLocal = out_.template DeQue<T>();
    LocalTensor<T> qLocal = dstLocal[0];
    LocalTensor<T> kLocal = dstLocal[stride_q];
    LocalTensor<T> vLocal = dstLocal[stride_q + stride_kv];

    // copy Q
    DataCopy(q_global_[q_dst_offset], qLocal, stride_q);

    // copy K cache
    DataCopy(k_global_[actual_dst_offset], kLocal, stride_kv);
    if (!incremental && is_prompt_cpy_) DataCopy(k_prompt_global_[kv_dst_offset], kLocal, stride_kv);

    // copy V cache
    DataCopy(v_global_[actual_dst_offset], vLocal, stride_kv);
    if (!incremental && is_prompt_cpy_) DataCopy(v_prompt_global_[kv_dst_offset], vLocal, stride_kv);

    out_.FreeTensor(dstLocal);
  }
  __aicore__ inline void GetTokenIdFromIdx(int idx, int *token_id) { *token_id = idx / head_num_; }
  __aicore__ inline void GetHeadIdIdFromIdx(int idx, int *head_id) { *head_id = idx % head_num_; }

  __aicore__ inline void GetQOffset(int token_id, int *offset) {
    bool incremental;
    int batch_id, seq_id;
    vsl_helper_.GetBatchId(token_id, &batch_id);
    vsl_helper_.GetSeqId(token_id, &seq_id);

    vsl_helper_.GetIncrementalMode(batch_id, &incremental);
    int cur_offset;
    vsl_helper_.GetActualOffset(batch_id, &cur_offset);
    *offset = cur_offset * head_size_ * head_num_;
    if (!incremental) {
      *offset += seq_id * head_size_ * head_num_;
    }
  }
  __aicore__ inline void GetKVOffset(int token_id, bool incremental, int *kv_offset, int *actual_offset) {
    int batch_id, seq_id;
    vsl_helper_.GetBatchId(token_id, &batch_id);
    vsl_helper_.GetSeqId(token_id, &seq_id);
    int actual_batch_id = batch_id;
    if (is_batch_2_batch_) {
      actual_batch_id = batch_to_batch_global_.GetValue(batch_id);
    }
    if (incremental) {
      int kv_seq_len;
      vsl_helper_.GetKVSeqLen(batch_id, &kv_seq_len);
      seq_id = kv_seq_len - 1;
    }
    int off = seq_id * head_size_ * kv_head_num_;
    if (paged_attention_) {
      int act_block_id = block_table_global_.GetValue(actual_batch_id * block_tbl_dim_ + seq_id / block_size_);
      off = (seq_id % block_size_) * head_size_ * kv_head_num_;
      int act_size = act_block_id * block_size_ * head_size_ * kv_head_num_;
      *actual_offset = off + act_size;
    } else {
      int act_size = actual_batch_id * max_seq_len_ * head_size_ * kv_head_num_;
      *actual_offset = off + act_size;
    }
    off = seq_id * head_size_ * kv_head_num_;
    int size = batch_id * max_seq_len_ * head_size_ * kv_head_num_;
    *kv_offset = off + size;
  }
  TPipe pipe_;
  TQue<QuePosition::VECIN, PipeSize> in_;
  TQue<QuePosition::VECOUT, PipeSize> out_;
  GlobalTensor<T> q_global_, k_global_, v_global_, qkv_global_, sin_global_, cos_global_;
  GlobalTensor<T> bias_global_, k_prompt_global_, v_prompt_global_;

  GlobalTensor<int> batch_to_batch_global_, block_table_global_;
  LocalTensor<T> q_local_, sin_local_, cos_local_;
  LocalTensor<T> bias_local_, k_local_, v_local_;
  TBuf<QuePosition::VECIN> bias_tmp_buf_, sin_tmp_buf_, cos_tmp_buf_;
  KernelVsl vsl_helper_;
  int batch_, max_seq_len_, head_num_, kv_head_num_, head_size_, actual_token_, block_size_, num_blocks_;
  int block_tbl_dim_;
  int total_blocks_, per_core_blocks_;
  int copy_size_;
  bool is_bias_;
  bool is_apply_rotary_;
  bool is_batch_2_batch_;
  bool is_prompt_cpy_;
  bool paged_attention_;
};

template <typename T, int PipeSize>
__aicore__ void KernelQKVPermuteOperator(GM_ADDR qkv_ptr, GM_ADDR bias_ptr, GM_ADDR q_ptr, GM_ADDR k_cache_ptr,
                                         GM_ADDR v_cache_ptr, VSLDescDT vsl_desc, GM_ADDR k_prompt, GM_ADDR v_prompt,
                                         GM_ADDR sin, GM_ADDR cos, GM_ADDR block_table, int actual_token,
                                         TransformerDescT desc_p, int total_blocks, int per_core_blocks) {
  KernelPermuteQKV<T, PipeSize> op;
  op.Init(qkv_ptr,      // qkv
          bias_ptr,     // bias
          q_ptr,        // q
          k_cache_ptr,  // k
          v_cache_ptr,  // v
          vsl_desc, k_prompt, v_prompt, sin, cos, block_table, actual_token, desc_p, total_blocks, per_core_blocks);
  op.Process();
}

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_QKV_PERMUTE_H_
