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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_SQUEEZE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_SQUEEZE_H_

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

template <uint32_t PipeSize, uint32_t ChunkSize, typename DataType>
class KernelSqueeze {
 public:
  __aicore__ inline KernelSqueeze() = default;
  __aicore__ inline void Init(GM_ADDR src, GM_ADDR dst, VSLDescDT vsl_desc, uint32_t elem_per_core,
                              uint32_t total_token, TransformerDescT desc_p) {
    vsl_helper_.Init(vsl_desc.act_q_seq_, vsl_desc.act_kv_seq_, vsl_desc.q_padding_, vsl_desc.kv_padding_,
                     vsl_desc.mode_per_batch_, total_token, desc_p.batch_size_, desc_p.seq_, &pipe_);
    elem_per_core_ = elem_per_core;
    total_token_ = total_token;
    head_size_ = desc_p.head_size_;
    head_num_ = desc_p.head_num_;
    seq_len_ = desc_p.seq_;
    batch_size_ = desc_p.batch_size_;
    int D = head_num_ * head_size_;
    actual_chunk_size_ = (ChunkSize > D) ? D : ChunkSize;
    chunk_num_ = UP_DIV(D, actual_chunk_size_);
    src_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(src), batch_size_ * seq_len_ * D);
    dst_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(dst), total_token_ * D);
    pipe_.InitBuffer(in_queue_, PipeSize, sizeof(DataType) * actual_chunk_size_);
    pipe_.InitBuffer(out_queue_, PipeSize, sizeof(DataType) * actual_chunk_size_);
  }

  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    for (size_t t = 0; t < elem_per_core_; t++) {
      int token_id = block_id * elem_per_core_ + t;
      if (token_id < total_token_) {
        int batch_id;
        bool incremental;
        vsl_helper_.GetBatchId(token_id, &batch_id);
        vsl_helper_.GetIncrementalMode(batch_id, &incremental);
        for (size_t c = 0; c < chunk_num_; c++) {
          uint32_t chunk_offset = c * actual_chunk_size_;
          uint32_t actual_elem = (head_size_ * head_num_) > (chunk_offset + actual_chunk_size_)
                                   ? actual_chunk_size_
                                   : (head_size_ * head_num_) - chunk_offset;
          uint32_t outOffset = token_id * head_size_ * head_num_ + chunk_offset;
          CopyInData(token_id, incremental, chunk_offset, actual_elem);
          Compute(actual_elem);
          CopyOut(outOffset, actual_elem);
        }
      }
    }
  }

 private:
  __aicore__ inline void GetPaddedOffset(int token_id, bool incremental, int *offset) {
    int batch_id, seq_id;
    vsl_helper_.GetBatchId(token_id, &batch_id);
    vsl_helper_.GetSeqId(token_id, &seq_id);

    int cur_offset;
    vsl_helper_.GetActualOffset(batch_id, &cur_offset);
    int off = cur_offset * head_size_ * head_num_;
    // B x S x H x d
    if (!incremental) {
      off += seq_id * head_size_ * head_num_;
    }
    *offset = off;
  }
  __aicore__ inline void CopyInData(uint32_t h_token_id, bool incremental, uint32_t chunk_offset,
                                    uint32_t actual_elem) {
    LocalTensor<DataType> input_x_local = in_queue_.template AllocTensor<DataType>();
    int offset;
    GetPaddedOffset(h_token_id, incremental, &offset);
    offset = offset + chunk_offset;
    DataCopy(input_x_local, src_global_[offset], actual_elem);
    in_queue_.template EnQue(input_x_local);
  }
  __aicore__ inline void Compute(uint32_t actual_elem) {
    LocalTensor<DataType> input_x_local = in_queue_.template DeQue<DataType>();
    LocalTensor<DataType> output_local = out_queue_.template AllocTensor<DataType>();
    DataCopy(output_local, input_x_local, actual_elem);
    out_queue_.template EnQue<DataType>(output_local);
    in_queue_.FreeTensor(input_x_local);
  }

  __aicore__ inline void CopyOut(int offset, uint32_t actual_elem) {
    LocalTensor<DataType> output_local = out_queue_.template DeQue<DataType>();
    DataCopy(dst_global_[offset], output_local, actual_elem);
    out_queue_.template FreeTensor(output_local);
  }

 private:
  GlobalTensor<DataType> src_global_;
  GlobalTensor<DataType> dst_global_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, PipeSize> in_queue_;
  TQue<QuePosition::VECOUT, PipeSize> out_queue_;
  uint32_t bufferSize_ = 0;
  uint32_t head_size_, head_num_, total_token_, batch_size_, seq_len_;
  uint32_t elem_per_core_;
  uint32_t chunk_num_;
  uint32_t actual_chunk_size_;
  KernelVsl vsl_helper_;
};

template <uint32_t PipeSize, uint32_t ChunkSize, typename DataType>
__aicore__ void KernelSqueezeOperator(GM_ADDR src, GM_ADDR dst, VSLDescDT vsl_desc, uint32_t elem_per_core,
                                      uint32_t total_token, TransformerDescT desc_p) {
  KernelSqueeze<PipeSize, ChunkSize, DataType> op;
  op.Init(src, dst, vsl_desc, elem_per_core, total_token, desc_p);
  op.Process();
}

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_SQUEEZE_H_
