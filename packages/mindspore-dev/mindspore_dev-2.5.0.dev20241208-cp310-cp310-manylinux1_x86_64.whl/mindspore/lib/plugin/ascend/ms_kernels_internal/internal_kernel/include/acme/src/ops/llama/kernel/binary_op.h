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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_BINARY_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_BINARY_OP_H_

#include "kernel_operator.h"
#include "kernel_utils.h"

template <typename T>
class kernelAdd {
 public:
  __aicore__ inline void Process(const LocalTensor<T> &dstLocal, const LocalTensor<T> &src0Local,
                                 const LocalTensor<T> &src1Local, const int32_t &calCount) {
    Add(dstLocal, src0Local, src1Local, calCount);
  }
};

template <int pipeSize, int blockSize, typename T, class binOp>
class KernelBinaryOp {
 public:
  __aicore__ inline KernelBinaryOp() = default;
  __aicore__ inline void Init(GM_ADDR in1, GM_ADDR in2, GM_ADDR out, uint32_t len, uint32_t len_per_core) {
    len_per_core_ = len_per_core;
    len_ = len;

    src1_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(in1), len_);
    src2_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(in2), len_);
    dst_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(out), len_);
    pipe_.InitBuffer(inQueueX1_, pipeSize, ALIGN32(blockSize * sizeof(T)));
    pipe_.InitBuffer(inQueueX2_, pipeSize, ALIGN32(blockSize * sizeof(T)));
    pipe_.InitBuffer(outQueue_, pipeSize, ALIGN32(blockSize * sizeof(T)));
  }
  __aicore__ inline void Process() {
    int blckId = GetBlockIdx();
    int start = blckId * len_per_core_;
    int end = (blckId + 1) * len_per_core_;

    if (start > len_) return;
    if (end > len_) end = len_;
    actual_len_per_core_ = end - start;

    int block_loop = actual_len_per_core_ / blockSize;
    int tail = actual_len_per_core_ % blockSize;

    for (size_t i = 0; i < block_loop; i++) {
      int offset = start + i * blockSize;
      CopyIn(offset, blockSize);
      Compute(blockSize);
      CopyOut(offset, blockSize);
    }

    if (tail) {
      int offset = start + block_loop * blockSize;
      CopyIn(offset, tail);
      Compute(tail);
      CopyOut(offset, tail);
    }
  }

 private:
  __aicore__ inline void CopyIn(uint32_t offset, uint32_t size) {
    LocalTensor<T> src1Local = inQueueX1_.template AllocTensor<T>();
    LocalTensor<T> src2Local = inQueueX2_.template AllocTensor<T>();

    uint32_t cpyElem = ALIGN32(size * sizeof(T)) / sizeof(T);
    DataCopy(src1Local, src1_global_[offset], cpyElem);
    DataCopy(src2Local, src2_global_[offset], cpyElem);
    inQueueX1_.EnQue(src1Local);
    inQueueX2_.EnQue(src2Local);
  }
  __aicore__ inline void Compute(uint32_t size) {
    LocalTensor<T> dstLocal = outQueue_.template AllocTensor<T>();
    LocalTensor<T> src1Local = inQueueX1_.template DeQue<T>();
    LocalTensor<T> src2Local = inQueueX2_.template DeQue<T>();
    op.Process(dstLocal, src1Local, src2Local, size);
    outQueue_.template EnQue<T>(dstLocal);
    inQueueX1_.FreeTensor(src1Local);
    inQueueX2_.FreeTensor(src2Local);
  }
  __aicore__ inline void CopyOut(uint32_t offset, uint32_t size) {
    LocalTensor<T> dstLocal = outQueue_.template DeQue<T>();
    uint32_t cpyElem = ALIGN32(size * sizeof(T)) / sizeof(T);
    DataCopy(dst_global_[offset], dstLocal, cpyElem);
    outQueue_.FreeTensor(dstLocal);
  }

 private:
  binOp op;
  GlobalTensor<T> src1_global_;
  GlobalTensor<T> src2_global_;
  GlobalTensor<T> dst_global_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, pipeSize> inQueueX1_;
  TQue<QuePosition::VECIN, pipeSize> inQueueX2_;
  TQue<QuePosition::VECOUT, pipeSize> outQueue_;
  uint32_t len_ = 0;
  uint32_t len_per_core_ = 0;
  uint32_t actual_len_per_core_ = 0;
};

template <int pipeSize, int ChunkSize, typename T>
class KernelAddScatter {
 public:
  __aicore__ inline KernelAddScatter() {}
  __aicore__ inline void Init(GM_ADDR in1, GM_ADDR in2, GM_ADDR out, uint32_t token_num, uint32_t hidden_size,
                              uint32_t elem_per_core, GM_ADDR token_to_token_gm) {
    elem_per_core_ = elem_per_core;
    token_num_ = token_num;
    hidden_size_ = hidden_size;
    actual_chunk_size_ = (ChunkSize > hidden_size) ? hidden_size : ChunkSize;
    chunk_num_ = UP_DIV(hidden_size, actual_chunk_size_);
    src1_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(in1), token_num * hidden_size);
    src2_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(in2), token_num * hidden_size);
    dst_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(out), token_num * hidden_size);
    is_scatter_ = (token_to_token_gm != nullptr);
    if (is_scatter_) {
      token_to_token_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(token_to_token_gm), token_num);
    }
    pipe_.InitBuffer(inQueueX1_, pipeSize, ALIGN32(actual_chunk_size_ * sizeof(T)));
    pipe_.InitBuffer(inQueueX2_, pipeSize, ALIGN32(actual_chunk_size_ * sizeof(T)));
    pipe_.InitBuffer(outQueue_, pipeSize, ALIGN32(actual_chunk_size_ * sizeof(T)));
  }
  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    for (size_t t = 0; t < elem_per_core_; t++) {
      int token_id = block_id * elem_per_core_ + t;
      int token_in_1 = token_id;
      if (token_id < token_num_) {
        if (is_scatter_) {
          token_in_1 = token_to_token_global_.GetValue(token_id);
        }
        for (size_t c = 0; c < chunk_num_; c++) {
          uint32_t chunk_offset = c * actual_chunk_size_;
          uint32_t actual_elem =
            hidden_size_ > (chunk_offset + actual_chunk_size_) ? actual_chunk_size_ : hidden_size_ - chunk_offset;
          int offset_in_1 = token_in_1 * hidden_size_ + chunk_offset;
          if (token_in_1 == -1) {
            offset_in_1 = -1;
          }
          uint32_t offset = token_id * hidden_size_ + chunk_offset;
          CopyIn(offset_in_1, offset, actual_elem);
          Compute(actual_elem, token_in_1);
          CopyOut(offset, actual_elem);
        }
      }
    }
  }

 private:
  __aicore__ inline void CopyIn(int offset_in_1, uint32_t offset, uint32_t size) {
    LocalTensor<T> src1Local = inQueueX1_.template AllocTensor<T>();
    LocalTensor<T> src2Local = inQueueX2_.template AllocTensor<T>();
    uint32_t cpyElem = ALIGN32(size * sizeof(T)) / sizeof(T);
    if (offset_in_1 != -1) {
      DataCopy(src1Local, src1_global_[offset_in_1], cpyElem);
    }
    DataCopy(src2Local, src2_global_[offset], cpyElem);
    inQueueX1_.EnQue(src1Local);
    inQueueX2_.EnQue(src2Local);
  }
  __aicore__ inline void Compute(uint32_t size, int token_id) {
    LocalTensor<T> dstLocal = outQueue_.template AllocTensor<T>();
    LocalTensor<T> src1Local = inQueueX1_.template DeQue<T>();
    LocalTensor<T> src2Local = inQueueX2_.template DeQue<T>();
    if (token_id != -1) {
      Add(dstLocal, src1Local, src2Local, size);
    } else {
      DataCopy(dstLocal, src2Local, size);
    }
    outQueue_.template EnQue<T>(dstLocal);
    inQueueX1_.FreeTensor(src1Local);
    inQueueX2_.FreeTensor(src2Local);
  }
  __aicore__ inline void CopyOut(uint32_t offset, uint32_t size) {
    LocalTensor<T> dstLocal = outQueue_.template DeQue<T>();
    uint32_t cpyElem = ALIGN32(size * sizeof(T)) / sizeof(T);
    DataCopy(dst_global_[offset], dstLocal, cpyElem);
    outQueue_.FreeTensor(dstLocal);
  }

 private:
  GlobalTensor<T> src1_global_;
  GlobalTensor<T> src2_global_;
  GlobalTensor<T> dst_global_;
  GlobalTensor<int> token_to_token_global_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, pipeSize> inQueueX1_;
  TQue<QuePosition::VECIN, pipeSize> inQueueX2_;
  TQue<QuePosition::VECOUT, pipeSize> outQueue_;
  uint32_t actual_chunk_size_ = 0;
  uint32_t chunk_num_ = 0;
  uint32_t elem_per_core_ = 0;
  uint32_t token_num_ = 0;
  uint32_t hidden_size_ = 0;
  bool is_scatter_ = false;
};

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_BINARY_OP_H_
