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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_ATTN_VEC_CORE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_ATTN_VEC_CORE_H_
#include <complex>
#include <math.h>
#include <cmath>
#include "kernel_operator.h"
#include "vsl_utils.h"
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
class KernelVocabEmbedding {
 public:
  __aicore__ inline KernelVocabEmbedding() = default;
  __aicore__ inline void Init(GM_ADDR position_idx, GM_ADDR embedding_table, GM_ADDR out, VSLDescDT vsl_desc,
                              uint32_t elem_per_core, uint32_t total_token, TransformerDescT desc) {
    vsl_helper_.Init(vsl_desc.act_q_seq_, vsl_desc.act_kv_seq_, vsl_desc.q_padding_, vsl_desc.kv_padding_,
                     vsl_desc.mode_per_batch_, total_token, desc.batch_size_, desc.seq_, &pipe_);
    elem_per_core_ = elem_per_core;
    total_token_ = total_token;
    size_t actual_hid_size = desc.head_num_ * desc.head_size_;
    hidden_size_ = actual_hid_size;
    batch_size_ = desc.batch_size_;
    seq_len_ = desc.seq_;
    actual_chunk_size_ = (ChunkSize > actual_hid_size) ? actual_hid_size : ChunkSize;
    chunk_num_ = UP_DIV(actual_hid_size, actual_chunk_size_);
    position_idx_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(position_idx), batch_size_ * seq_len_);
    embedding_table_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(embedding_table),
                                            seq_len_ * hidden_size_);
    out_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(out), total_token_ * hidden_size_);
    pipe_.InitBuffer(embedding_table_queue_, PipeSize, sizeof(DataType) * actual_chunk_size_);
    pipe_.InitBuffer(out_queue_, PipeSize, sizeof(DataType) * actual_chunk_size_);
  }

  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    for (size_t t = 0; t < elem_per_core_; t++) {
      uint32_t token_id = block_id * elem_per_core_ + t;
      if (token_id < total_token_) {
        for (size_t c = 0; c < chunk_num_; c++) {
          uint32_t chunk_offset = c * actual_chunk_size_;
          uint32_t actual_elem =
            hidden_size_ > (chunk_offset + actual_chunk_size_) ? actual_chunk_size_ : hidden_size_ - chunk_offset;
          uint32_t offset = token_id * hidden_size_ * 3 + chunk_offset;
          CopyInData(token_id, chunk_offset, actual_elem);
          Compute(actual_elem);
          CopyOut(offset, actual_elem);
        }
      }
    }
  }

 private:
  __aicore__ inline void GetPaddedOffset(int token_id, int *offset) {
    int batch_id, seq_id;
    bool is_inc;
    vsl_helper_.GetBatchId(token_id, &batch_id);
    vsl_helper_.GetIncrementalMode(batch_id, &is_inc);
    vsl_helper_.GetSeqId(token_id, &seq_id);
    *offset = batch_id * seq_len_ + seq_id;
  }
  __aicore__ inline void CopyInData(uint32_t h_token_id, int32_t chunk_offset, uint32_t actual_elem) {
    LocalTensor<DataType> embedding_table_local = embedding_table_queue_.template AllocTensor<DataType>();
    int in_offset;
    GetPaddedOffset(h_token_id, &in_offset);
    int token = position_idx_global_.GetValue(in_offset);
    int offset = token * hidden_size_ + chunk_offset;
    DataCopy(embedding_table_local, embedding_table_global_[offset], actual_elem);
    embedding_table_queue_.template EnQue(embedding_table_local);
  }
  __aicore__ inline void Compute(uint32_t actual_elem) {
    LocalTensor<DataType> embedding_table_local = embedding_table_queue_.template DeQue<DataType>();
    LocalTensor<DataType> output_local = out_queue_.template AllocTensor<DataType>();
    DataCopy(output_local, embedding_table_local, actual_elem);
    out_queue_.template EnQue<DataType>(output_local);
    embedding_table_queue_.FreeTensor(embedding_table_local);
  }

  __aicore__ inline void CopyOut(int offset, uint32_t actual_elem) {
    LocalTensor<DataType> output_local = out_queue_.template DeQue<DataType>();
    DataCopy(out_global_[offset], output_local, actual_elem);
    out_queue_.template FreeTensor(output_local);
  }

 private:
  GlobalTensor<DataType> position_idx_global_;
  GlobalTensor<DataType> embedding_table_global_;
  GlobalTensor<DataType> out_global_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, PipeSize> embedding_table_queue_;
  TQue<QuePosition::VECOUT, PipeSize> out_queue_;
  uint32_t bufferSize_ = 0;
  uint32_t hidden_size_, total_token_, batch_size_, seq_len_;
  uint32_t elem_per_core_;
  uint32_t chunk_num_;
  uint32_t actual_chunk_size_;
  KernelVsl vsl_helper_;
};

template <uint32_t PipeSize, uint32_t ChunkSize, typename DataType>
__aicore__ void KernelVocabEmbeddingOperator(GM_ADDR position_idx, GM_ADDR embedding_table, GM_ADDR out,
                                             VSLDescDT vsl_desc, uint32_t elem_per_core, uint32_t total_token,
                                             TransformerDescT desc) {
  KernelVocabEmbedding<PipeSize, ChunkSize, DataType> op;
  op.Init(position_idx, embedding_table, out, vsl_desc, elem_per_core, total_token, desc);
  op.Process();
}

// gather
template <uint32_t PipeSize, uint32_t ChunkSize, typename DataType>
class KernelGatherHead {
 public:
  __aicore__ inline KernelGatherHead() = default;
  __aicore__ inline void Init(GM_ADDR src_gm, GM_ADDR dst_gm, uint32_t elem_per_core, uint32_t total_token,
                              TransformerDescT p_desc, VSLDescDT vsl_desc) {
    vsl_helper_.Init(vsl_desc.act_q_seq_, vsl_desc.act_kv_seq_, vsl_desc.q_padding_, vsl_desc.kv_padding_,
                     vsl_desc.mode_per_batch_, total_token, p_desc.batch_size_, p_desc.seq_, &pipe_);
    elem_per_core_ = elem_per_core;
    total_token_ = total_token;
    hidden_size_ = p_desc.hid_dim_;
    batch_size_ = p_desc.batch_size_;
    actual_chunk_size_ = (ChunkSize > hidden_size_) ? hidden_size_ : ChunkSize;
    chunk_num_ = UP_DIV(hidden_size_, actual_chunk_size_);
    src_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(src_gm), total_token * hidden_size_);
    dst_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(dst_gm), batch_size_ * hidden_size_);
    is_gather_by_batch_to_batch_ = (vsl_desc.batch_to_batch_ == nullptr) ? false : true;
    if (is_gather_by_batch_to_batch_) {
      batch_to_batch_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(vsl_desc.batch_to_batch_), batch_size_);
    }
    pipe_.InitBuffer(src_queue_, PipeSize, sizeof(DataType) * actual_chunk_size_);
    pipe_.InitBuffer(dst_queue_, PipeSize, sizeof(DataType) * actual_chunk_size_);
  }

  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    for (size_t t = 0; t < elem_per_core_; t++) {
      uint32_t batch_id = block_id * elem_per_core_ + t;
      if (batch_id < batch_size_) {
        for (size_t c = 0; c < chunk_num_; c++) {
          uint32_t chunk_offset = c * actual_chunk_size_;
          uint32_t actual_elem =
            hidden_size_ > (chunk_offset + actual_chunk_size_) ? actual_chunk_size_ : hidden_size_ - chunk_offset;
          CopyInData(batch_id, chunk_offset, actual_elem);
          Compute(actual_elem);
          int actual_batch_id = batch_id;
          if (is_gather_by_batch_to_batch_) {
            actual_batch_id = batch_to_batch_global_.GetValue(batch_id);
          }
          uint32_t offset = actual_batch_id * hidden_size_ + chunk_offset;
          CopyOut(offset, actual_elem);
        }
      }
    }
  }

 private:
  __aicore__ inline void GetInOffset(int batch_id, int *offset) {
    int token_id, seq_len;
    vsl_helper_.GetTokenIdByBatch(batch_id, &token_id);
    vsl_helper_.GetSeqLen(batch_id, &seq_len);
    *offset = (token_id + seq_len - 1) * hidden_size_;
  }
  __aicore__ inline void CopyInData(uint32_t batch_id, int32_t chunk_offset, uint32_t actual_elem) {
    LocalTensor<DataType> src_local = src_queue_.template AllocTensor<DataType>();
    int in_offset;
    GetInOffset(batch_id, &in_offset);
    DataCopy(src_local, src_global_[in_offset], actual_elem);
    src_queue_.template EnQue(src_local);
  }
  __aicore__ inline void Compute(uint32_t actual_elem) {
    LocalTensor<DataType> src_local = src_queue_.template DeQue<DataType>();
    LocalTensor<DataType> dst_local = dst_queue_.template AllocTensor<DataType>();
    DataCopy(dst_local, src_local, actual_elem);
    dst_queue_.template EnQue<DataType>(dst_local);
    src_queue_.FreeTensor(src_local);
  }

  __aicore__ inline void CopyOut(int offset, uint32_t actual_elem) {
    LocalTensor<DataType> dst_local = dst_queue_.template DeQue<DataType>();
    DataCopy(dst_global_[offset], dst_local, actual_elem);
    dst_queue_.template FreeTensor(dst_local);
  }

 private:
  GlobalTensor<DataType> src_global_;
  GlobalTensor<DataType> dst_global_;
  GlobalTensor<int> batch_to_batch_global_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, PipeSize> src_queue_;
  TQue<QuePosition::VECOUT, PipeSize> dst_queue_;
  uint32_t hidden_size_, total_token_, batch_size_, seq_len_;
  uint32_t elem_per_core_;
  uint32_t chunk_num_;
  uint32_t actual_chunk_size_;
  bool is_gather_by_batch_to_batch_;
  KernelVsl vsl_helper_;
};

template <uint32_t PipeSize, uint32_t ChunkSize, typename DataType>
__aicore__ void KernelGatherHeadOperator(GM_ADDR src_gm, GM_ADDR dst_gm, uint32_t elem_per_core, uint32_t total_token,
                                         TransformerDescT p_desc, VSLDescDT vsl_desc) {
  KernelGatherHead<PipeSize, ChunkSize, DataType> op;
  op.Init(src_gm, dst_gm, elem_per_core, total_token, p_desc, vsl_desc);
  op.Process();
}

/// create token to token and expert count
class KernelCreateCountExpert {
 public:
  __aicore__ inline KernelCreateCountExpert() {}
  __aicore__ inline void Init(GM_ADDR expert_ids, GM_ADDR out, GM_ADDR seq_lens, GM_ADDR padding_offset, GM_ADDR mode,
                              uint32_t moe_num, uint32_t expert_num, float capacity, uint32_t batch_size,
                              uint32_t seq_len, uint32_t moe_id, bool is_query, uint32_t elem_per_core) {
    vsl_helper_.Init(seq_lens, seq_lens, padding_offset, padding_offset, mode, batch_size * seq_len, batch_size,
                     seq_len, &pipe_);
    seq_len_ = seq_len;
    batch_size_ = batch_size;
    expert_num_ = expert_num;
    elem_per_core_ = elem_per_core;
    moe_id_ = moe_id;
    is_query_ = is_query;
    max_capacity_ = UP_DIV((capacity * seq_len), expert_num);
    expert_ids_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(expert_ids), moe_num * batch_size_ * seq_len_);
    out_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(out), batch_size * expert_num);
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    pipe_.InitBuffer(expert_ids_queue_, 1, ALIGN32(sizeof(int) * seq_len_));
    pipe_.InitBuffer(count_tmp_, sizeof(int) * align_expert_num);
    pipe_.InitBuffer(expert_count_queue_, 1, sizeof(int) * align_expert_num);
    count_tmp_local_ = count_tmp_.Get<int>();
  }

  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    for (size_t t = 0; t < elem_per_core_; t++) {
      uint32_t batch_id = block_id * elem_per_core_ + t;
      if (batch_id < batch_size_) {
        CopyInData(batch_id);
        LocalTensor<int> expert_ids_local = expert_ids_queue_.template DeQue<int>();
        Muls(count_tmp_local_, count_tmp_local_, 0, align_expert_num);
        int actual_seq;
        vsl_helper_.GetSeqLen(batch_id, &actual_seq);
        actual_seq = (is_query_) ? actual_seq - 1 : actual_seq;
        int expert_id_last_token = expert_ids_local.GetValue(actual_seq);
        for (size_t seq_id = 0; seq_id < actual_seq; seq_id++) {
          int expert_id = expert_ids_local.GetValue(seq_id);
          int cur_count = count_tmp_local_.GetValue(expert_id);
          if (!(expert_id >= expert_num_ || expert_id < 0)) {
            if (cur_count < max_capacity_) {
              if (!(is_query_ && (expert_id_last_token != expert_id))) {
                count_tmp_local_.SetValue(expert_id, cur_count + 1);
              }
            }
          }
        }
        // if is_query calculate the last token only
        if (is_query_) {
          int cur_count = count_tmp_local_.GetValue(expert_id_last_token);
          if (!(expert_id_last_token >= expert_num_ || expert_id_last_token < 0)) {
            if (cur_count < max_capacity_) {
              count_tmp_local_.SetValue(expert_id_last_token, 1);
            } else {
              count_tmp_local_.SetValue(expert_id_last_token, 0);
            }
          }
        }
        LocalTensor<int> dst_local = expert_count_queue_.template AllocTensor<int>();
        DataCopy(dst_local, count_tmp_local_, align_expert_num);
        expert_count_queue_.template EnQue(dst_local);
        CopyOutData(batch_id);
        pipe_barrier(PIPE_ALL);
        expert_ids_queue_.FreeTensor(expert_ids_local);
      }
    }
  }
  __aicore__ inline void CopyInData(int batch_id) {
    LocalTensor<int> expert_local = expert_ids_queue_.template AllocTensor<int>();
    bool is_inc;
    vsl_helper_.GetIncrementalMode(batch_id, &is_inc);
    int seq = (is_inc) ? 1 : seq_len_;
    if (is_inc) {
      expert_local.SetValue(0, expert_ids_global_.GetValue(moe_id_ * batch_size_ * seq + batch_id * seq));
    } else {
      DataCopy(expert_local, expert_ids_global_[moe_id_ * batch_size_ * seq + batch_id * seq],
               ALIGN32(seq * sizeof(int)) / sizeof(int));
    }
    expert_ids_queue_.template EnQue(expert_local);
  }

  __aicore__ inline void CopyOutData(int batch_id) {
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    LocalTensor<int> dst_local = expert_count_queue_.template DeQue<int>();
    DataCopy(out_global_[batch_id * align_expert_num], dst_local, align_expert_num);
    expert_count_queue_.FreeTensor(dst_local);
  }

 private:
  GlobalTensor<int> expert_ids_global_;
  GlobalTensor<int> out_global_;
  TQue<QuePosition::VECIN, 1> expert_ids_queue_;
  TQue<QuePosition::VECOUT, 1> expert_count_queue_;
  TBuf<QuePosition::VECCALC> count_tmp_;
  LocalTensor<int> count_tmp_local_;
  TPipe pipe_;
  uint32_t expert_num_ = 0;
  uint32_t batch_size_ = 0;
  uint32_t seq_len_ = 0;
  uint32_t moe_id_ = 0;
  int max_capacity_ = 0;
  uint32_t elem_per_core_ = 0;
  bool is_query_ = false;
  KernelVsl vsl_helper_;
};

class KernelCreateMoeParam {
 public:
  __aicore__ inline KernelCreateMoeParam() {}
  __aicore__ inline void Init(GM_ADDR expert_ids, GM_ADDR expert_count_by_batch, GM_ADDR expert_count,
                              GM_ADDR token_to_token, GM_ADDR seq_lens, GM_ADDR padding_offset, GM_ADDR mode,
                              uint32_t expert_num, uint32_t moe_num, uint32_t batch_size, uint32_t seq_len,
                              uint32_t total_token, uint32_t moe_id, float capacity, bool is_query,
                              uint32_t elem_per_core) {
    vsl_helper_.Init(seq_lens, seq_lens, padding_offset, padding_offset, mode, total_token, batch_size, seq_len,
                     &pipe_);
    seq_len_ = seq_len;
    batch_size_ = batch_size;
    expert_num_ = expert_num;
    elem_per_core_ = elem_per_core;
    moe_id_ = moe_id;
    is_query_ = is_query;
    inc_max_capacity_ = UP_DIV((capacity * batch_size), expert_num);
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    expert_ids_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(expert_ids), moe_num * batch_size_ * seq_len_);
    expert_count_by_batch_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(expert_count_by_batch),
                                                  batch_size_ * expert_num);
    token_to_token_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(token_to_token), batch_size_ * seq_len_);
    expert_count_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(expert_count), expert_num);
    pipe_.InitBuffer(expert_count_tmp_, sizeof(int) * align_expert_num * batch_size_);
    expert_count_tmp_local_ = expert_count_tmp_.Get<int>();
    pipe_.InitBuffer(count_tmp_, sizeof(int) * align_expert_num);
    count_tmp_local_ = count_tmp_.Get<int>();
    pipe_.InitBuffer(expert_by_batch_queue_, 1, sizeof(int) * align_expert_num * batch_size_);
    pipe_.InitBuffer(expert_count_queue_, 1, sizeof(int) * align_expert_num);
    pipe_.InitBuffer(expert_ids_queue_, 1, ALIGN32(sizeof(int) * seq_len_));
  }

  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    bool is_inc;
    vsl_helper_.GetIncrementalMode(0, &is_inc);
    CopyInCountExpert();
    LocalTensor<int> expert_count_by_batch_local = expert_by_batch_queue_.template DeQue<int>();
    // calculate count tokens per expert to 0...batch_id
    DataCopy(expert_count_tmp_local_, expert_count_by_batch_local, align_expert_num);
    for (size_t i = 1; i < batch_size_; i++) {
      Add(expert_count_tmp_local_[i * align_expert_num], expert_count_by_batch_local[i * align_expert_num],
          expert_count_tmp_local_[(i - 1) * align_expert_num], align_expert_num);
    }

    for (size_t t = 0; t < elem_per_core_; t++) {
      uint32_t batch_id = block_id * elem_per_core_ + t;
      if (batch_id < batch_size_) {
        CopyInExpertIds(batch_id);
        LocalTensor<int> expert_ids_local = expert_ids_queue_.template DeQue<int>();
        Muls(count_tmp_local_, count_tmp_local_, 0, align_expert_num);
        // copy out count tokens per expert
        if (batch_id == 0) {
          LocalTensor<int> dst_local = expert_count_queue_.template AllocTensor<int>();
          DataCopy(dst_local, expert_count_tmp_local_[(batch_size_ - 1) * align_expert_num], align_expert_num);
          expert_count_queue_.template EnQue(dst_local);
          CopyOutData();
        }
        int actual_seq;
        // get actual seq for current batch
        vsl_helper_.GetSeqLen(batch_id, &actual_seq);
        int current_token_not_expert = 0;
        for (size_t seq_id = 0; seq_id < actual_seq; seq_id++) {
          // get expert id to current token
          int seq = (is_inc) ? 1 : seq_len_;
          int expert_id = expert_ids_local.GetValue(seq_id);
          bool is_expert;
          // check if expert id is valid
          is_expert = !(expert_id >= expert_num_ || expert_id < 0);
          // not expert if inc and there is token expert to expert_id until
          // current batch current seq_id
          is_expert = is_expert && !(is_inc && batch_id > 0 &&
                                     expert_count_tmp_local_.GetValue((batch_id - 1) * align_expert_num + expert_id) +
                                         count_tmp_local_.GetValue(expert_id) >
                                       inc_max_capacity_ - 1);
          // not expert if is query and the it's not the last token (useless)
          is_expert = is_expert && !(is_query_ && seq_id < actual_seq - 1);
          // not expert if expert id for current batch pass max capacity
          // (expert_count_by_batch_local include the max tokens per batch and
          // expert)
          is_expert = is_expert && (count_tmp_local_.GetValue(expert_id) <
                                    expert_count_by_batch_local.GetValue(batch_id * expert_num_ + expert_id));
          if (is_expert) {
            // calculate token id after gather for expert
            SetTokenId(batch_id, seq_id, expert_id, is_inc);
          } else {
            // set -1 for token_id after gather for token that will not expert
            int token_offset;
            vsl_helper_.GetTokenIdByBatch(batch_id, &token_offset);
            token_to_token_global_.SetValue(token_offset + seq_id, -1);
          }
        }
        pipe_barrier(PIPE_ALL);
        expert_ids_queue_.FreeTensor(expert_ids_local);
      }
    }
    pipe_barrier(PIPE_ALL);
    expert_by_batch_queue_.FreeTensor(expert_count_by_batch_local);
  }
  __aicore__ inline void CopyInCountExpert() {
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    LocalTensor<int> expert_local = expert_by_batch_queue_.template AllocTensor<int>();
    DataCopy(expert_local, expert_count_by_batch_global_, align_expert_num * batch_size_);
    expert_by_batch_queue_.template EnQue(expert_local);
  }
  __aicore__ inline void SetTokenId(int batch_id, int seq_id, int expert_id, bool is_inc) {
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    int token_id = 0;
    // add count tokens until current expert id
    for (size_t i = 0; i < expert_id; i++) {
      int expert_count = expert_count_tmp_local_.GetValue((batch_size_ - 1) * align_expert_num + i);
      token_id += (is_inc && expert_count > 0) ? (expert_count > inc_max_capacity_) ? inc_max_capacity_ : expert_count
                                               : expert_count;
    }
    if (batch_id > 0) {
      // add count tokens for expert id until current batch
      token_id += expert_count_tmp_local_.GetValue((batch_id - 1) * align_expert_num + expert_id);
    }
    // add count tokens for expert id in batch id until current token
    int cur_count = count_tmp_local_.GetValue(expert_id);
    token_id += cur_count;
    count_tmp_local_.SetValue(expert_id, cur_count + 1);
    // calculate current token offset in compress data
    int token_offset;
    vsl_helper_.GetTokenIdByBatch(batch_id, &token_offset);
    token_to_token_global_.SetValue(token_offset + seq_id, token_id);
  }
  __aicore__ inline void CopyOutData() {
    int align_expert_num = ALIGN32(sizeof(int) * expert_num_) / sizeof(int);
    LocalTensor<int> dst_local = expert_count_queue_.template DeQue<int>();
    DataCopy(expert_count_global_, dst_local, align_expert_num);
    expert_count_queue_.FreeTensor(dst_local);
  }
  __aicore__ inline void CopyInExpertIds(int batch_id) {
    LocalTensor<int> expert_local = expert_ids_queue_.template AllocTensor<int>();
    bool is_inc;
    vsl_helper_.GetIncrementalMode(batch_id, &is_inc);
    int seq = (is_inc) ? 1 : seq_len_;
    if (is_inc) {
      expert_local.SetValue(0, expert_ids_global_.GetValue(moe_id_ * batch_size_ * seq + batch_id * seq));
    } else {
      DataCopy(expert_local, expert_ids_global_[moe_id_ * batch_size_ * seq + batch_id * seq],
               ALIGN32(seq * sizeof(int)) / sizeof(int));
    }
    expert_ids_queue_.template EnQue(expert_local);
  }

 private:
  GlobalTensor<int> expert_ids_global_;
  GlobalTensor<int> expert_count_global_;
  GlobalTensor<int> token_to_token_global_;
  GlobalTensor<int> expert_count_by_batch_global_;
  TQue<QuePosition::VECIN, 1> expert_by_batch_queue_;
  TQue<QuePosition::VECOUT, 1> expert_count_queue_;
  TQue<QuePosition::VECIN, 1> expert_ids_queue_;
  TPipe pipe_;
  uint32_t expert_num_ = 0;
  uint32_t batch_size_ = 0;
  uint32_t seq_len_ = 0;
  uint32_t moe_id_ = 0;
  int inc_max_capacity_ = 0;
  uint32_t elem_per_core_ = 0;
  bool is_query_ = false;
  KernelVsl vsl_helper_;
  TBuf<QuePosition::VECCALC> count_tmp_, expert_count_tmp_;
  LocalTensor<int> count_tmp_local_, expert_count_tmp_local_;
};

template <uint32_t PipeSize, uint32_t ChunkSize, typename DataType>
class KernelNormalizationDistAttn {
 public:
  __aicore__ inline KernelNormalizationDistAttn() = default;
  __aicore__ inline void Init(GM_ADDR src, GM_ADDR dst, GM_ADDR softmax_max, GM_ADDR softmax_sum,
                              GM_ADDR softmax_max_out, GM_ADDR softmax_sum_out, VSLDescDT vsl_desc,
                              uint32_t elem_per_core, uint32_t total_token, TransformerDescT desc_p, int dist_size) {
    vsl_helper_.Init(vsl_desc.act_q_seq_, vsl_desc.act_kv_seq_, vsl_desc.q_padding_, vsl_desc.kv_padding_,
                     vsl_desc.mode_per_batch_, total_token, desc_p.batch_size_, desc_p.seq_, &pipe_);
    elem_per_core_ = elem_per_core;
    total_token_ = total_token;
    head_size_ = desc_p.head_size_;
    head_num_ = desc_p.head_num_;
    seq_len_ = desc_p.seq_;
    batch_size_ = desc_p.batch_size_;
    dist_size_ = dist_size;
    int D = head_num_ * head_size_;
    src_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(src), dist_size_ * total_token_ * D);
    dst_global_.SetGlobalBuffer(reinterpret_cast<__gm__ DataType *>(dst), total_token_ * D);
    max_global_.SetGlobalBuffer(reinterpret_cast<__gm__ float *>(softmax_max),
                                dist_size_ * total_token_ * head_num_ * 8);
    sum_global_.SetGlobalBuffer(reinterpret_cast<__gm__ float *>(softmax_sum),
                                dist_size_ * total_token_ * head_num_ * 8);
    pipe_.InitBuffer(in_queue_, PipeSize, sizeof(DataType) * head_size_);
    pipe_.InitBuffer(out_queue_, PipeSize, sizeof(DataType) * head_size_);
    pipe_.InitBuffer(max_queue_, PipeSize, ALIGN32(sizeof(float) * 8));
    pipe_.InitBuffer(sum_queue_, PipeSize, ALIGN32(sizeof(float) * 8));
    pipe_.InitBuffer(tmp_, PipeSize, ALIGN32(sizeof(float) * head_size_ * dist_size_));
    tmp_local_ = tmp_.template AllocTensor<float>();
    pipe_.InitBuffer(tmp2_, PipeSize, ALIGN32(sizeof(DataType) * head_size_));
    tmp_half_ = tmp2_.template AllocTensor<DataType>();
    softmax_out_ = (softmax_max_out != nullptr);
    if (softmax_out_) {
      max_out_global_.SetGlobalBuffer(reinterpret_cast<__gm__ float *>(softmax_max_out), total_token_ * head_num_ * 8);
      sum_out_global_.SetGlobalBuffer(reinterpret_cast<__gm__ float *>(softmax_sum_out), total_token_ * head_num_ * 8);
      pipe_.InitBuffer(max_out_queue_, PipeSize, sizeof(float) * 8);
      pipe_.InitBuffer(sum_out_queue_, PipeSize, sizeof(float) * 8);
    }
    int stack_total_elem = 0;
    PopStackBuffer<float, AscendC::TPosition::VECCALC>(stackBuffer_);
    reduce_out_local_ = stackBuffer_[stack_total_elem];
    stack_total_elem += ALIGN(dist_size_, 8);
    tmp_sum_local_ = stackBuffer_[stack_total_elem];
    stack_total_elem += ALIGN(dist_size_, 8);
    tmp_max_local_ = stackBuffer_[stack_total_elem];
    stack_total_elem += ALIGN(dist_size_, 8);
    tmp_act_max_local_ = stackBuffer_[stack_total_elem];
    stack_total_elem += ALIGN(dist_size_, 8);
    reduce_tmp_local_ = stackBuffer_[stack_total_elem];
  }

  __aicore__ inline void Process() {
    int block_id = GetBlockIdx();
    for (size_t t = 0; t < elem_per_core_; t++) {
      int elem_id = block_id * elem_per_core_ + t;
      int head_id = elem_id % head_num_;
      int token_id = elem_id / head_num_;
      if (token_id < total_token_) {
        for (size_t i = 0; i < dist_size_; i++) {
          CopyInData(token_id, head_id, i, head_size_);
          Compute(i, head_size_);
        }
        pipe_barrier(PIPE_V);
        ComputeSumAndMax();
        for (size_t i = 0; i < dist_size_; i++) {
          ComputeOut(i, head_size_);
        }
        uint32_t out_offset = token_id * head_size_ * head_num_ + head_id * head_size_;
        uint32_t out_sofmax_offset = token_id * head_num_ * 8 + head_id * 8;
        CopyOut(out_offset, out_sofmax_offset, head_size_);
      }
    }
  }

 private:
  __aicore__ inline void CopyInData(uint32_t h_token_id, uint32_t head_id, int dist_id, uint32_t actual_elem) {
    LocalTensor<DataType> input_x_local = in_queue_.template AllocTensor<DataType>();
    LocalTensor<float> input_max_local = max_queue_.template AllocTensor<float>();
    LocalTensor<float> input_sum_local = sum_queue_.template AllocTensor<float>();
    int offset =
      h_token_id * dist_size_ * head_num_ * head_size_ + dist_id * head_num_ * head_size_ + head_id * head_size_;
    DataCopy(input_x_local, src_global_[offset], actual_elem);
    int offset_softmax = h_token_id * dist_size_ * head_num_ * 8 + dist_id * head_num_ * 8 + head_id * 8;
    DataCopy(input_max_local, max_global_[offset_softmax], 8);
    DataCopy(input_sum_local, sum_global_[offset_softmax], 8);
    in_queue_.template EnQue(input_x_local);
    max_queue_.template EnQue(input_max_local);
    sum_queue_.template EnQue(input_sum_local);
  }
  __aicore__ inline void Compute(uint32_t dist_id, uint32_t actual_elem) {
    LocalTensor<DataType> input_x_local = in_queue_.template DeQue<DataType>();
    LocalTensor<float> input_max_local = max_queue_.template DeQue<float>();
    LocalTensor<float> input_sum_local = sum_queue_.template DeQue<float>();
    float cur_max;
    if (softmax_out_) {
      cur_max = input_max_local.GetValue(0);
      set_flag(PIPE_MTE3, PIPE_V, EVENT_ID0);
      wait_flag(PIPE_MTE3, PIPE_V, EVENT_ID0);
      tmp_act_max_local_.SetValue(dist_id, cur_max);
    }
    Exp(input_max_local, input_max_local, 8);
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    cur_max = input_max_local.GetValue(0);
    float cur_sum = input_sum_local.GetValue(0);
    float sum = cur_sum * cur_max;
    Cast(tmp_local_[dist_id * actual_elem], input_x_local, AscendC::RoundMode::CAST_NONE, actual_elem);
    pipe_barrier(PIPE_V);
    Muls(tmp_local_[dist_id * actual_elem], tmp_local_[dist_id * actual_elem], cur_sum, actual_elem);
    pipe_barrier(PIPE_V);
    Muls(tmp_local_[dist_id * actual_elem], tmp_local_[dist_id * actual_elem], cur_max, actual_elem);
    tmp_sum_local_.SetValue(dist_id, sum);
    tmp_max_local_.SetValue(dist_id, cur_max);
    in_queue_.FreeTensor(input_x_local);
    max_queue_.FreeTensor(input_max_local);
    sum_queue_.FreeTensor(input_sum_local);
  }
  __aicore__ inline void ComputeSumAndMax() {
    ReduceSum(reduce_out_local_, tmp_sum_local_, reduce_tmp_local_, dist_size_);
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    sum_ = reduce_out_local_.GetValue(0);
    ReduceMax(reduce_out_local_, tmp_max_local_, reduce_tmp_local_, dist_size_);
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    max_ = reduce_out_local_.GetValue(0);
    max_ = 1.0f / max_;
    sum_ = sum_ * max_;
    if (softmax_out_) {
      LocalTensor<float> output_max_local = max_out_queue_.template AllocTensor<float>();
      LocalTensor<float> output_sum_local = sum_out_queue_.template AllocTensor<float>();
      ReduceMax(reduce_out_local_, tmp_act_max_local_, reduce_tmp_local_, dist_size_);
      set_flag(PIPE_V, PIPE_S, EVENT_ID0);
      wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
      act_max_ = reduce_out_local_.GetValue(0);
      Muls(output_max_local, output_max_local, (float)0.0f, 8);
      Muls(output_sum_local, output_sum_local, (float)0.0f, 8);
      pipe_barrier(PIPE_V);
      Adds(output_sum_local, output_sum_local, sum_, 8);
      Adds(output_max_local, output_max_local, act_max_, 8);
      max_out_queue_.template EnQue(output_max_local);
      sum_out_queue_.template EnQue(output_sum_local);
    }
    sum_ = 1.0f / sum_;
    LocalTensor<DataType> output_local = out_queue_.template AllocTensor<DataType>();
    Muls(output_local, output_local, (DataType)0, head_size_);
    out_queue_.template EnQue(output_local);
  }
  __aicore__ inline void ComputeOut(uint32_t dist_id, uint32_t actual_elem) {
    LocalTensor<DataType> output_local = out_queue_.template DeQue<DataType>();
    Muls(tmp_local_[dist_id * actual_elem], tmp_local_[dist_id * actual_elem], max_, actual_elem);
    pipe_barrier(PIPE_V);
    Muls(tmp_local_[dist_id * actual_elem], tmp_local_[dist_id * actual_elem], sum_, actual_elem);
    pipe_barrier(PIPE_V);
    Cast(tmp_half_, tmp_local_[dist_id * actual_elem], AscendC::RoundMode::CAST_NONE, actual_elem);
    pipe_barrier(PIPE_V);
    Add(output_local, output_local, tmp_half_, actual_elem);
    out_queue_.template EnQue<DataType>(output_local);
  }
  __aicore__ inline void CopyOut(int offset, int softmax_out_offset, uint32_t actual_elem) {
    LocalTensor<DataType> output_local = out_queue_.template DeQue<DataType>();
    DataCopy(dst_global_[offset], output_local, actual_elem);
    out_queue_.template FreeTensor(output_local);
    if (softmax_out_) {
      LocalTensor<float> output_max_local = max_out_queue_.template DeQue<float>();
      DataCopy(max_out_global_[softmax_out_offset], output_max_local, 8);
      max_out_queue_.template FreeTensor(output_max_local);

      LocalTensor<float> output_sum_local = sum_out_queue_.template DeQue<float>();
      DataCopy(sum_out_global_[softmax_out_offset], output_sum_local, 8);
      sum_out_queue_.template FreeTensor(output_sum_local);
    }
  }

 private:
  GlobalTensor<DataType> src_global_;
  GlobalTensor<DataType> dst_global_;
  GlobalTensor<float> sum_global_, sum_out_global_;
  GlobalTensor<float> max_global_, max_out_global_;
  TPipe pipe_;
  TQue<QuePosition::VECIN, PipeSize> in_queue_;
  TQue<QuePosition::VECOUT, PipeSize> out_queue_;
  TQue<QuePosition::VECIN, PipeSize> sum_queue_, sum_out_queue_;
  TQue<QuePosition::VECIN, PipeSize> max_queue_, max_out_queue_;
  TQue<QuePosition::VECCALC, PipeSize> tmp_;
  TQue<QuePosition::VECCALC, PipeSize> tmp2_;
  LocalTensor<float> tmp_local_;
  LocalTensor<DataType> tmp_half_;
  LocalTensor<float> reduce_out_local_;
  LocalTensor<float> reduce_tmp_local_;
  LocalTensor<float> tmp_sum_local_;
  LocalTensor<float> tmp_max_local_;
  LocalTensor<float> tmp_act_max_local_;
  LocalTensor<float> stackBuffer_;

  uint32_t bufferSize_ = 0;
  uint32_t head_size_, head_num_, total_token_, batch_size_, seq_len_, dist_size_;
  float max_, sum_, act_max_;
  bool softmax_out_;
  uint32_t elem_per_core_;
  uint32_t chunk_num_;
  uint32_t actual_chunk_size_;
  KernelVsl vsl_helper_;
};

template <uint32_t PipeSize, uint32_t ChunkSize, typename DataType>
__aicore__ void KernelNormalizationDistAttnOperator(GM_ADDR src, GM_ADDR dst, GM_ADDR softmax_max, GM_ADDR softmax_sum,
                                                    GM_ADDR softmax_max_out, GM_ADDR softmax_sum_out,
                                                    VSLDescDT vsl_desc, uint32_t elem_per_core, uint32_t total_token,
                                                    TransformerDescT desc_p, int dist_size) {
  KernelNormalizationDistAttn<PipeSize, ChunkSize, DataType> op;
  op.Init(src, dst, softmax_max, softmax_sum, softmax_max_out, softmax_sum_out, vsl_desc, elem_per_core, total_token,
          desc_p, dist_size);
  op.Process();
}

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_ATTN_VEC_CORE_H_
