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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_NORMALIZATION_RMS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_NORMALIZATION_RMS_H_

#include "kernel_operator.h"
#include "vsl_utils.h"
using AscendC::AIV;
using AscendC::GlobalTensor;
using AscendC::LocalTensor;
using AscendC::QuePosition;
using AscendC::TBuf;
using AscendC::TPipe;
using AscendC::TQue;

template <uint32_t pipeSize, uint32_t chunkSize, typename T, typename S = T>
class KernelRMSNorm {
 public:
  __aicore__ inline KernelRMSNorm() {}
  __aicore__ inline uint32_t InitReduceWorkspaceSize() {
    constexpr int block_size = 32;
    constexpr int repeat_size = 256;
    int type_size = sizeof(float);
    // Number of elements a block can hold
    int elements_per_block = block_size / type_size;
    // Number of elements that can be processed in a repeat
    int elements_per_repeat = repeat_size / type_size;
    int first_max_repeat = UP_DIV(actual_chunk_size_, elements_per_repeat);
    int iter1_align_end = UP_DIV(first_max_repeat, elements_per_block) * elements_per_block;
    return iter1_align_end;
  }
  __aicore__ inline void Init(GM_ADDR inputx_gm, GM_ADDR inputy_gm, GM_ADDR gamma_gm, GM_ADDR output_gm,
                              GM_ADDR output_norm_gm, GM_ADDR input_ids_gm, GM_ADDR emmbeding_word_gm,
                              uint32_t token_per_block, uint32_t total_token, float h_length_float,
                              TransformerDescT p_desc, VSLDescDT vsl_desc) {
    int blckId = GetBlockIdx();
    token_per_block_ = token_per_block;
    total_token_ = total_token;
    h_length_ = p_desc.hid_dim_;
    epsilon_ = p_desc.ln_eps_;
    float_h_length_ = h_length_float;
    actual_chunk_size_ = (chunkSize > h_length_) ? h_length_ : chunkSize;
    chunk_num_ = UP_DIV(h_length_, actual_chunk_size_);
    batch_size_ = p_desc.batch_size_;
    uint32_t input_size = h_length_ * total_token_;
    uint32_t reduce_work_space_size = InitReduceWorkspaceSize();
    seq_length_ = p_desc.seq_;
    // Setup global pointers
    is_embedding_ = (input_ids_gm != nullptr);
    if (!is_embedding_) {
      inputx_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(inputx_gm), input_size);
    }
    gamma_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(gamma_gm), h_length_);
    output_norm_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(output_norm_gm), input_size);
    is_residual_ = (inputy_gm != nullptr);
    if (is_residual_) {
      inputy_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(inputy_gm), input_size);
      pipe_.InitBuffer(in_queue_y_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
      output_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(output_gm), input_size);
      pipe_.InitBuffer(out_queue_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
    }
    if (is_embedding_) {
      vsl_helper_.Init(vsl_desc.act_q_seq_, vsl_desc.act_kv_seq_, vsl_desc.q_padding_, vsl_desc.kv_padding_,
                       vsl_desc.mode_per_batch_, total_token, p_desc.batch_size_, p_desc.seq_, &pipe_);
      output_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(output_gm), h_length_ * total_token_);
      pipe_.InitBuffer(out_queue_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
      input_ids_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(input_ids_gm), total_token_);
      emmbeding_word_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(emmbeding_word_gm),
                                             p_desc.vocab_size_ * h_length_);
      pipe_.InitBuffer(in_embedd_queue_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
      batch_to_batch_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(vsl_desc.batch_to_batch_), batch_size_);
    }
    pipe_.InitBuffer(in_queue_x_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
    pipe_.InitBuffer(out_norm_queue_, pipeSize, ALIGN32(sizeof(S) * actual_chunk_size_));
    pipe_.InitBuffer(x_tmp_, pipeSize, ALIGN32(sizeof(S) * h_length_));

    x_tmp_local_ = x_tmp_.template AllocTensor<S>();
    pipe_.InitBuffer(in_buf_gamma_, ALIGN32(sizeof(T) * h_length_));
    gamma_tmp_local_ = in_buf_gamma_.Get<T>();

    int stack_total_elem = 0;
    PopStackBuffer<float, AscendC::TPosition::VECCALC>(stackBuffer_);
    cast_tmp_local_ = stackBuffer_[stack_total_elem];
    stack_total_elem += ALIGN(actual_chunk_size_, 8);
    reduce_tmp_local_ = stackBuffer_[stack_total_elem];
    stack_total_elem += ALIGN(reduce_work_space_size, 8);
    reduce_output_tmp_local_ = stackBuffer_[stack_total_elem];
    stack_total_elem += ALIGN(actual_chunk_size_, 8);
    if constexpr (sizeof(S) == sizeof(float)) {
      gamma_float_ = stackBuffer_[stack_total_elem];
      stack_total_elem += ALIGN(h_length_, 8);
    }
  }
  __aicore__ inline void Process() {
    int blckId = GetBlockIdx();
    CopyInWeight();
    LocalTensor<T> ping_pong_local_arr[pipeSize];
    for (size_t t = 0; t < token_per_block_; t++) {
      uint32_t token_id = blckId * token_per_block_ + t;
      LocalTensor<T> &ping_pong_local = ping_pong_local_arr[token_id % pipeSize];
      if (token_id < total_token_) {
        sum_of_squares_ = 0.0f;
        for (size_t c = 0; c < chunk_num_; c++) {
          uint32_t chunk_offset = c * actual_chunk_size_;
          uint32_t actual_elem =
            h_length_ > (chunk_offset + actual_chunk_size_) ? actual_chunk_size_ : h_length_ - chunk_offset;
          CopyInData(token_id, c, actual_elem);
          ComputeReduction(c, actual_elem, ping_pong_local);
          CopyOut(token_id * ALIGN_BY_TYPE(h_length_, sizeof(T), 32) + chunk_offset, actual_elem);
        }
        ComputeMeanAndVar();
        for (size_t c = 0; c < chunk_num_; c++) {
          uint32_t chunk_offset = c * actual_chunk_size_;
          uint32_t actual_elem =
            h_length_ > (chunk_offset + actual_chunk_size_) ? actual_chunk_size_ : h_length_ - chunk_offset;
          Normalize(c, actual_elem, ping_pong_local);
          CopyNormOut(token_id * ALIGN_BY_TYPE(h_length_, sizeof(T), 32) + chunk_offset, actual_elem);
        }
      }
    }
  }

 private:
  __aicore__ inline void CopyInWeight() {
    DataCopy(gamma_tmp_local_, gamma_global_, ALIGN_BY_TYPE(h_length_, sizeof(T), 32));
    if constexpr (sizeof(S) == sizeof(float)) {
      // make sure gamma is ready to use
      set_flag(PIPE_MTE2, PIPE_V, EVENT_ID3);
      wait_flag(PIPE_MTE2, PIPE_V, EVENT_ID3);
      Cast(gamma_float_, gamma_tmp_local_, AscendC::RoundMode::CAST_NONE, h_length_);
    }
  }

  __aicore__ inline void CopyInData(uint32_t token_id, uint32_t chunk_id, uint32_t actual_elem) {
    LocalTensor<T> inputx_local = in_queue_x_.template AllocTensor<T>();
    if (is_embedding_) {
      int batch_id, seq_id, q_seq_len;
      bool is_inc = false;
      vsl_helper_.GetBatchId(token_id, &batch_id);
      vsl_helper_.GetSeqId(token_id, &seq_id);
      vsl_helper_.GetIncrementalMode(batch_id, &is_inc);
      int act_batch_id = batch_to_batch_global_.GetValue(batch_id);
      int offset = 0;
      for (size_t i = 0; i < batch_size_; i++) {
        if (batch_to_batch_global_.GetValue(i) < act_batch_id) {
          int bvl;
          vsl_helper_.GetSeqLen(i, &bvl);
          offset += bvl;
        }
      }
      int32_t embedding_offset =
        input_ids_global_.GetValue(offset + seq_id) * h_length_ + chunk_id * actual_chunk_size_;
      DataCopy(inputx_local, emmbeding_word_global_[embedding_offset], ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    } else {
      DataCopy(inputx_local,
               inputx_global_[token_id * ALIGN_BY_TYPE(h_length_, sizeof(T), 32) + chunk_id * actual_chunk_size_],
               ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    }
    if (is_residual_) {
      LocalTensor<T> inputy_local = in_queue_y_.template AllocTensor<T>();
      DataCopy(inputy_local,
               inputy_global_[token_id * ALIGN_BY_TYPE(h_length_, sizeof(T), 32) + chunk_id * actual_chunk_size_],
               ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
      in_queue_y_.template EnQue(inputy_local);
    }
    in_queue_x_.template EnQue(inputx_local);
  }

  __aicore__ inline void ComputeReduction(uint32_t chunk_id, uint32_t actual_elem, LocalTensor<T> &ping_pong_local) {
    uint32_t chunk_offset = chunk_id * actual_chunk_size_;
    LocalTensor<T> inputx_local = in_queue_x_.template DeQue<T>();
    LocalTensor<T> inputy_local;

    if (is_residual_) {
      LocalTensor<T> output_local = out_queue_.template AllocTensor<T>();
      inputy_local = in_queue_y_.template DeQue<T>();
      Add(inputx_local, inputx_local, inputy_local, actual_elem);
      // Add(output_local, inputx_local, inputy_local, actual_elem);
      pipe_barrier(PIPE_V);
      DataCopy(output_local, inputx_local, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
      out_queue_.template EnQue<T>(output_local);
    }
    if (is_embedding_) {
      LocalTensor<T> output_local = out_queue_.template AllocTensor<T>();
      DataCopy(output_local, inputx_local, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
      out_queue_.template EnQue<T>(output_local);
    }

    if constexpr (sizeof(S) == sizeof(half)) {
      if (chunk_num_ > 1) {
        DataCopy(x_tmp_local_[chunk_offset], inputx_local, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
      } else {
        ping_pong_local = inputx_local[0];
      }
    }

    Cast(cast_tmp_local_, inputx_local, AscendC::RoundMode::CAST_NONE, actual_elem);
    if constexpr (sizeof(S) == sizeof(float)) {
      pipe_barrier(PIPE_ALL);
      DataCopy(x_tmp_local_[chunk_offset], cast_tmp_local_, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    }

    // do sigma^2
    Mul(cast_tmp_local_, cast_tmp_local_, cast_tmp_local_, actual_elem);
    ReduceSum(reduce_output_tmp_local_, cast_tmp_local_, reduce_tmp_local_, actual_elem);
    pipe_barrier(PIPE_V);  // syncronize before Get Value
    sum_of_squares_ += reduce_output_tmp_local_.GetValue(0);

    if (chunk_num_ > 1) {
      in_queue_x_.FreeTensor(inputx_local);
    }
    if (is_residual_) {
      in_queue_y_.FreeTensor(inputy_local);
    }
  }

  __aicore__ inline void ComputeMeanAndVar() {
    float rms = sum_of_squares_ / float_h_length_;
    rms_ = (S)(1.0f / static_cast<float>(sqrt(rms + static_cast<float>(epsilon_))));
  }

  __aicore__ inline void Normalize(uint32_t chunk_id, uint32_t actual_elem, LocalTensor<T> &ping_pong_local) {
    LocalTensor<S> output_norm_local = out_norm_queue_.template AllocTensor<S>();
    // normalize tensor
    if (chunk_num_ > 1) {
      Muls(output_norm_local, x_tmp_local_[chunk_id * actual_chunk_size_], rms_, actual_elem);
    } else {
      Muls(output_norm_local, ping_pong_local, rms_, actual_elem);
    }
    // Mul with Gamma and add bias
    if constexpr (sizeof(S) == sizeof(float)) {
      Mul(output_norm_local, output_norm_local, gamma_float_, actual_elem);
    } else {
      Mul(output_norm_local, output_norm_local, gamma_tmp_local_, actual_elem);
    }
    if (chunk_num_ == 1) {
      in_queue_x_.FreeTensor(ping_pong_local);
    }
    out_norm_queue_.template EnQue<S>(output_norm_local);
  }

  __aicore__ inline void CopyOut(int offset, uint32_t actual_elem) {
    if (is_residual_ || is_embedding_) {
      LocalTensor<T> output_local_ = out_queue_.template DeQue<T>();
      DataCopy(output_global_[offset], output_local_, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
      out_queue_.template FreeTensor(output_local_);
    }
  }

  __aicore__ inline void CopyNormOut(int offset, uint32_t actual_elem) {
    LocalTensor<S> output_norm_local = out_norm_queue_.template DeQue<S>();
    if constexpr (sizeof(S) == sizeof(float)) {
      Cast(gamma_tmp_local_, output_norm_local, AscendC::RoundMode::CAST_NONE, actual_elem);
      pipe_barrier(PIPE_ALL);
      DataCopy(output_norm_global_[offset], gamma_tmp_local_, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    } else {
      DataCopy(output_norm_global_[offset], output_norm_local, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    }
    out_norm_queue_.template FreeTensor(output_norm_local);
  }

 private:
  GlobalTensor<T> inputx_global_;
  GlobalTensor<T> inputy_global_;
  GlobalTensor<int> input_ids_global_, batch_to_batch_global_;
  GlobalTensor<T> gamma_global_;
  GlobalTensor<T> emmbeding_word_global_;
  GlobalTensor<T> output_global_;
  GlobalTensor<T> output_norm_global_;

  LocalTensor<float> cast_tmp_local_;
  LocalTensor<float> reduce_sum_of_sqr_tmp_local_, reduce_output_tmp_local_, reduce_tmp_local_;
  LocalTensor<T> gamma_tmp_local_;
  LocalTensor<S> x_tmp_local_;
  KernelVsl vsl_helper_;
  LocalTensor<float> stackBuffer_;
  LocalTensor<float> gamma_float_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, pipeSize> in_queue_x_;
  TQue<QuePosition::VECIN, pipeSize> in_queue_y_;
  TQue<QuePosition::VECIN, pipeSize> in_embedd_queue_;
  TQue<QuePosition::VECOUT, pipeSize> out_queue_;
  TQue<QuePosition::VECOUT, pipeSize> out_norm_queue_;

  TQue<QuePosition::VECCALC, pipeSize> x_tmp_;
  TBuf<QuePosition::VECIN> in_buf_gamma_;

  bool is_residual_;
  bool is_embedding_;
  uint32_t token_per_block_;
  uint32_t total_token_;
  uint32_t batch_size_;
  uint32_t chunk_num_;
  uint32_t actual_chunk_size_;
  int seq_length_;
  uint32_t h_length_;
  T epsilon_;
  float float_h_length_;
  float sum_of_squares_;
  S rms_;
};

template <uint32_t pipeSize, uint32_t chunkSize, typename T>
__aicore__ void KernelRMSNormOperator(GM_ADDR inputx_gm, GM_ADDR inputy_gm, GM_ADDR gamma_gm, GM_ADDR output_gm,
                                      GM_ADDR output_norm_gm, GM_ADDR input_ids_gm, GM_ADDR emmbeding_word_gm,
                                      uint32_t token_num, uint32_t total_token, float float_h_length,
                                      TransformerDescT p_desc, VSLDescDT vsl_desc) {
  if (g_coreType == AIV) {
    KernelRMSNorm<pipeSize, chunkSize, T, T> op;
    op.Init(inputx_gm, inputy_gm, gamma_gm, output_gm, output_norm_gm, input_ids_gm, emmbeding_word_gm, token_num,
            total_token, float_h_length, p_desc, vsl_desc);
    op.Process();
  }
}
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_NORMALIZATION_RMS_H_
