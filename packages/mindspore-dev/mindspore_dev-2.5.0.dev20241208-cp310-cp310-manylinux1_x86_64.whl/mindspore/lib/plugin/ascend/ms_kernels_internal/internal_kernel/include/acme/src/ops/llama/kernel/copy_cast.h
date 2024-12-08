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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_COPY_CAST_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_COPY_CAST_H_

#include "kernel_operator.h"
#include "kernel_utils.h"

template <int pipeSize, int blockSize, typename srcType, typename dstType>
class KernelCopyCast {
 public:
  __aicore__ inline KernelCopyCast() = default;
  __aicore__ inline void Init(GM_ADDR src_gm, GM_ADDR dst_gm, uint32_t token_num, uint32_t token_per_core) {
    token_per_core_ = token_per_core;
    token_num_ = token_num;

    src_global_.SetGlobalBuffer(reinterpret_cast<__gm__ srcType *>(src_gm), token_num_);
    dst_global_.SetGlobalBuffer(reinterpret_cast<__gm__ dstType *>(dst_gm), token_num_);
    pipe_.InitBuffer(inQueueX_, pipeSize, ALIGN32(blockSize * sizeof(srcType)));
    pipe_.InitBuffer(outQueue_, pipeSize, ALIGN32(blockSize * sizeof(dstType)));
  }

  __aicore__ inline void Process() {
    int blckId = AscendC::GetBlockIdx();
    int start = blckId * token_per_core_;
    int end = (blckId + 1) * token_per_core_;

    if (start > token_num_) return;
    if (end > token_num_) end = token_num_;
    actual_token_per_core_ = end - start;

    int block_loop = actual_token_per_core_ / blockSize;
    int tail = actual_token_per_core_ % blockSize;
    // per block cast
    for (size_t i = 0; i < block_loop; i++) {
      int offset = start + i * blockSize;
      copyIn(offset, blockSize);
      compute(blockSize);
      copyOut(offset, blockSize);
    }
    // tail cast
    if (tail) {
      int offset = start + block_loop * blockSize;
      copyIn(offset, tail);
      compute(tail);
      copyOut(offset, tail);
    }
  }

 private:
  __aicore__ inline void copyIn(uint32_t offset, uint32_t size) {
    AscendC::LocalTensor<srcType> srcLocal = inQueueX_.template AllocTensor<srcType>();
    uint32_t cpyElem = ALIGN32(size * sizeof(srcType)) / sizeof(srcType);
    DataCopy(srcLocal, src_global_[offset], cpyElem);
    inQueueX_.EnQue(srcLocal);
  }

  __aicore__ inline void compute(uint32_t size) {
    AscendC::LocalTensor<dstType> dstLocal = outQueue_.template AllocTensor<dstType>();
    AscendC::LocalTensor<srcType> srcLocal = inQueueX_.template DeQue<srcType>();
    Cast(dstLocal, srcLocal, AscendC::RoundMode::CAST_NONE, size);
    outQueue_.template EnQue<dstType>(dstLocal);
    inQueueX_.FreeTensor(srcLocal);
  }

  __aicore__ inline void copyOut(uint32_t offset, uint32_t size) {
    AscendC::LocalTensor<dstType> dstLocal = outQueue_.template DeQue<dstType>();
    uint32_t cpyElem = ALIGN32(size * sizeof(dstType)) / sizeof(dstType);
    DataCopy(dst_global_[offset], dstLocal, cpyElem);
    outQueue_.FreeTensor(dstLocal);
  }

 private:
  AscendC::GlobalTensor<srcType> src_global_;
  AscendC::GlobalTensor<dstType> dst_global_;
  AscendC::TPipe pipe_;
  AscendC::TQue<AscendC::QuePosition::VECIN, pipeSize> inQueueX_;
  AscendC::TQue<AscendC::QuePosition::VECOUT, pipeSize> outQueue_;
  uint32_t token_num_ = 0;
  uint32_t token_per_core_ = 0;
  uint32_t actual_token_per_core_ = 0;
};

template <int pipeSize, int blockSize, typename srcType, typename dstType>
__aicore__ void kernel_copy_cast_operator(GM_ADDR src_gm, GM_ADDR dst_gm, uint32_t token_number,
                                          uint32_t tokenPerCore) {
  KernelCopyCast<pipeSize, blockSize, srcType, dstType> op;
  op.Init(src_gm, dst_gm, token_number, tokenPerCore);
  op.Process();
}

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_COPY_CAST_H_
