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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_SILU_MUL_FUSE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_SILU_MUL_FUSE_H_

#include "kernel_operator.h"
#include "kernel_utils.h"

using AscendC::GetBlockIdx;
using AscendC::GetBlockNum;
using AscendC::GlobalTensor;
using AscendC::LocalTensor;
using AscendC::QuePosition;
using AscendC::TBuf;
using AscendC::TPipe;
using AscendC::TQue;

template <uint32_t pipeSize, typename T>
class KernelSiluAndMul {
 public:
  __aicore__ inline KernelSiluAndMul() {}
  __aicore__ inline void Init(GM_ADDR input_gm, GM_ADDR output_gm, uint32_t elem_per_block, uint32_t total_token,
                              uint32_t h_length, uint32_t chunkSize, uint32_t elem_per_token) {
    elem_per_block_ = elem_per_block;
    elem_per_token_ = elem_per_token;
    total_token_ = total_token;
    h_length_ = h_length;
    stride_ = h_length_;
    work_len_ = h_length_ / elem_per_token_;
    actual_chunk_size_ = (chunkSize > work_len_) ? work_len_ : chunkSize;
    chunk_num_ = UP_DIV(work_len_, actual_chunk_size_);
    uint32_t input_size = 2 * stride_ * total_token_;
    uint32_t out_size = stride_ * total_token_;
    input_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(input_gm), input_size);
    output_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(output_gm), out_size);
    pipe_.InitBuffer(in_x_queue_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
    pipe_.InitBuffer(in_y_queue_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
    pipe_.InitBuffer(out_queue_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
    pipe_.InitBuffer(x_tmp_, pipeSize, ALIGN32(sizeof(T) * actual_chunk_size_));
  }
  __aicore__ inline void Process() {
    int blckId = GetBlockIdx();

    for (size_t t = 0; t < elem_per_block_; t++) {
      // uint32_t elem_id = blckId * elem_per_block_ + t;
      uint32_t elem_id = (blckId * elem_per_block_ + t) % elem_per_token_;
      uint32_t token_id = (blckId * elem_per_block_ + t) / elem_per_token_;
      if (token_id < total_token_) {
        for (size_t c = 0; c < chunk_num_; c++) {
          uint32_t chunk_offset = c * actual_chunk_size_;
          uint32_t actual_elem =
            work_len_ > (chunk_offset + actual_chunk_size_) ? actual_chunk_size_ : work_len_ - chunk_offset;
          uint32_t offset = token_id * 2 * stride_ + elem_id * work_len_ + chunk_offset;
          CopyInData(offset, actual_elem);
          Compute(c, actual_elem);
          uint32_t out_offset = token_id * stride_ + elem_id * work_len_ + chunk_offset;
          CopyOut(out_offset, actual_elem);
        }
      }
    }
  }

 private:
  __aicore__ inline void CopyInData(uint32_t offset, uint32_t actual_elem) {
    LocalTensor<T> input_x_local = in_x_queue_.template AllocTensor<T>();
    LocalTensor<T> input_y_local = in_y_queue_.template AllocTensor<T>();
    DataCopy(input_x_local, input_global_[offset], ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    DataCopy(input_y_local, input_global_[offset + h_length_], ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    in_x_queue_.template EnQue(input_x_local);
    in_y_queue_.template EnQue(input_y_local);
  }
  __aicore__ inline void Compute(uint32_t chunk_id, uint32_t actual_elem) {
    LocalTensor<T> input_x_local = in_x_queue_.template DeQue<T>();
    LocalTensor<T> input_y_local = in_y_queue_.template DeQue<T>();
    LocalTensor<T> output_local = out_queue_.template AllocTensor<T>();
    LocalTensor<T> x_tmp_local = x_tmp_.template AllocTensor<T>();
    Sigmoid(x_tmp_local, input_x_local, actual_elem);
    Mul(x_tmp_local, input_x_local, x_tmp_local, actual_elem);
    Mul(output_local, input_y_local, x_tmp_local, actual_elem);
    out_queue_.template EnQue<T>(output_local);
    in_x_queue_.FreeTensor(input_x_local);
    in_y_queue_.FreeTensor(input_y_local);
    x_tmp_.FreeTensor(x_tmp_local);
  }

  __aicore__ inline void CopyOut(int offset, uint32_t actual_elem) {
    LocalTensor<T> output_local_ = out_queue_.template DeQue<T>();
    DataCopy(output_global_[offset], output_local_, ALIGN_BY_TYPE(actual_elem, sizeof(T), 32));
    out_queue_.template FreeTensor(output_local_);
  }

 private:
  GlobalTensor<T> input_global_;

  GlobalTensor<T> output_global_;
  LocalTensor<T> x_tmp_local_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, pipeSize> in_x_queue_;
  TQue<QuePosition::VECIN, pipeSize> in_y_queue_;
  TQue<QuePosition::VECOUT, pipeSize> out_queue_;
  TQue<QuePosition::VECCALC, pipeSize> x_tmp_;
  uint32_t elem_per_block_ = 0;
  uint32_t elem_per_token_ = 0;
  uint32_t total_token_ = 0;
  uint32_t chunk_num_ = 0;
  uint32_t actual_chunk_size_ = 0;
  uint32_t h_length_ = 0;
  uint32_t stride_ = 0;
  uint32_t work_len_ = 0;
};

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_SILU_MUL_FUSE_H_
