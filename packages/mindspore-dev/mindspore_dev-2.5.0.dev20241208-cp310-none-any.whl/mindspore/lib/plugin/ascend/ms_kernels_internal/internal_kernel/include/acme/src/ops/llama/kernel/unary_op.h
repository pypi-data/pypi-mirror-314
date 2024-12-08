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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_UNARY_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_UNARY_OP_H_

#include "kernel_operator.h"
#include "kernel_utils.h"

template <typename T>
class KernelFastGelu {
 public:
  __aicore__ inline void Process(const AscendC::LocalTensor<T> &dstLocal, const AscendC::LocalTensor<T> &srcLocal,
                                 const int32_t &calCount) {
    FasterGelu(dstLocal, srcLocal, calCount);
  }
};

template <int pipeSize, int blockSize, typename T, class UnaryOp>
class KernelUnaryOp {
 public:
  __aicore__ inline KernelUnaryOp() {}
  __aicore__ inline void Init(GM_ADDR in, GM_ADDR out, uint32_t len, uint32_t len_per_core) {
    len_per_core_ = len_per_core;
    len_ = len;

    src_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(in), len_);
    dst_global_.SetGlobalBuffer(reinterpret_cast<__gm__ T *>(out), len_);
    pipe_.InitBuffer(inQueue_, pipeSize, ALIGN32(blockSize * sizeof(T)));
    pipe_.InitBuffer(outQueue_, pipeSize, ALIGN32(blockSize * sizeof(T)));
  }
  __aicore__ inline void Process() {
    int blckId = AscendC::GetBlockIdx();
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
    AscendC::LocalTensor<T> srcLocal = inQueue_.template AllocTensor<T>();

    uint32_t cpyElem = ALIGN32(size * sizeof(T)) / sizeof(T);
    DataCopy(srcLocal, src_global_[offset], cpyElem);
    inQueue_.EnQue(srcLocal);
  }
  __aicore__ inline void Compute(uint32_t size) {
    AscendC::LocalTensor<T> dstLocal = outQueue_.template AllocTensor<T>();
    AscendC::LocalTensor<T> srcLocal = inQueue_.template DeQue<T>();
    op.Process(dstLocal, srcLocal, size);
    outQueue_.template EnQue<T>(dstLocal);
    inQueue_.FreeTensor(srcLocal);
  }
  __aicore__ inline void CopyOut(uint32_t offset, uint32_t size) {
    AscendC::LocalTensor<T> dstLocal = outQueue_.template DeQue<T>();
    uint32_t cpyElem = ALIGN32(size * sizeof(T)) / sizeof(T);
    DataCopy(dst_global_[offset], dstLocal, cpyElem);
    outQueue_.FreeTensor(dstLocal);
  }

 private:
  UnaryOp op;
  AscendC::GlobalTensor<T> src_global_;
  AscendC::GlobalTensor<T> dst_global_;
  AscendC::TPipe pipe_;
  AscendC::TQue<AscendC::QuePosition::VECIN, pipeSize> inQueue_;
  AscendC::TQue<AscendC::QuePosition::VECOUT, pipeSize> outQueue_;
  uint32_t len_ = 0;
  uint32_t len_per_core_ = 0;
  uint32_t actual_len_per_core_ = 0;
};

template <int pipeSize, int blockSize, typename T, class UnaryOp>
__aicore__ void kernel_unary_operator(GM_ADDR in, GM_ADDR out, int len) {
  int tot_block_num = AscendC::GetBlockNum();
  int len_per_core = ALIGN32((ALIGN(len, blockSize) / tot_block_num));
  KernelUnaryOp<pipeSize, blockSize, T, UnaryOp> op;
  op.Init(in, out, len, len_per_core);
  op.Process();
}
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_UNARY_OP_H_
