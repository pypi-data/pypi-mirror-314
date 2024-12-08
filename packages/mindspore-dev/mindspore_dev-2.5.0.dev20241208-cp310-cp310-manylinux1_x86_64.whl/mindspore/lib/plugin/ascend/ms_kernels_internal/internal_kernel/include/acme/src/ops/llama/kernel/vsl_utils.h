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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_VSL_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_VSL_UTILS_H_

#include "kernel_operator.h"
#include "kernel_utils.h"

using AscendC::AIV;
using AscendC::GetBlockIdx;
using AscendC::GlobalTensor;
using AscendC::LocalTensor;
using AscendC::QuePosition;
using AscendC::TBuf;
using AscendC::TPipe;
using AscendC::TQue;

typedef struct VSLDescDT {
  GM_ADDR act_q_seq_ = nullptr;
  GM_ADDR act_kv_seq_ = nullptr;
  GM_ADDR q_padding_ = nullptr;
  GM_ADDR kv_padding_ = nullptr;
  GM_ADDR mode_per_batch_ = nullptr;
  GM_ADDR batch_to_batch_ = nullptr;
  GM_ADDR token_to_token_ = nullptr;
} VSLDescDT;
class KernelVsl {
 public:
  __aicore__ inline KernelVsl() = default;
  __aicore__ inline void CopyVSL(KernelVsl *vsl_helper, __gm__ KernelVsl *vsl_helper_gm) {
    uint32_t *ptr = reinterpret_cast<uint32_t *>(vsl_helper);
    auto vsl_helper_32 = reinterpret_cast<__gm__ uint32_t *>(vsl_helper_gm);

    for (size_t i = 0; i < sizeof(KernelVsl) / sizeof(uint32_t); i++, ptr++) {
      *ptr = *(vsl_helper_32 + i);
    }
    return;
  }
  __aicore__ inline void CopyPipe(TPipe *pipe, __gm__ TPipe *pipe_gm) {
    uint32_t *ptr = reinterpret_cast<uint32_t *>(pipe);
    auto pipe_32 = reinterpret_cast<__gm__ uint32_t *>(pipe_gm);

    for (size_t i = 0; i < sizeof(TPipe) / sizeof(uint32_t); i++, ptr++) {
      *ptr = *(pipe_32 + i);
    }
    return;
  }
  __aicore__ inline void Init(GM_ADDR q_seq_len, GM_ADDR kv_seq_len, GM_ADDR q_padding_offset,
                              GM_ADDR kv_padding_offset, GM_ADDR mode, int actual_token, int batch, int seq_len,
                              TPipe *pipe) {
    max_token_ = batch * seq_len;
    actual_token_ = actual_token;
    seq_len_ = seq_len;
    batch_ = batch;
    pipe_ = pipe;

    q_padding_offset_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(q_padding_offset), max_token_);
    kv_padding_offset_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(kv_padding_offset), max_token_);
    q_seq_len_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(q_seq_len), batch_);
    kv_seq_len_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(kv_seq_len), batch_);
    mode_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(mode), batch_);
    pipe_->InitBuffer(q_seq_len_local_ptr_, ALIGN32(batch_ * sizeof(int)));
    pipe_->InitBuffer(kv_seq_len_local_ptr_, ALIGN32(batch_ * sizeof(int)));
    pipe_->InitBuffer(mode_local_ptr_, ALIGN32(batch_ * sizeof(int)));

    q_seq_len_local_ = q_seq_len_local_ptr_.Get<int>();
    kv_seq_len_local_ = kv_seq_len_local_ptr_.Get<int>();
    mode_local_ = mode_local_ptr_.Get<int>();

    // copy need to be align to 32 bytes according to type (8 int's are 32 bytes)
    DataCopy(q_seq_len_local_, q_seq_len_global_, ALIGN(batch_, 8));
    DataCopy(kv_seq_len_local_, kv_seq_len_global_, ALIGN(batch_, 8));
    DataCopy(mode_local_, mode_global_, ALIGN(batch_, 8));
    pipe_barrier(PIPE_ALL);
  }

  __aicore__ inline void GetBatchId(int token_id, int *batch_id) {
    *batch_id = (q_padding_offset_global_.GetValue(token_id) + token_id) / seq_len_;
  }

  __aicore__ inline void GetSeqLen(int batch_id, int *act_seq_len) {
    *act_seq_len = q_seq_len_local_.GetValue(batch_id);
  }
  __aicore__ inline void GetKVSeqLen(int batch_id, int *act_seq_len) {
    *act_seq_len = kv_seq_len_local_.GetValue(batch_id);
  }

  __aicore__ inline void GetSeqId(int token_id, int *seq_id) {
    *seq_id = (q_padding_offset_global_.GetValue(token_id) + token_id) % seq_len_;
  }
  __aicore__ inline void GetPositionIdByTokenId(int token_id, int *position_id) {
    int cur_token_id = token_id;
    int i = 0;
    *position_id = 0;
    for (; i < batch_; i++) {
      if (cur_token_id < q_seq_len_local_.GetValue(i)) {
        *position_id = cur_token_id;
        break;
      }
      cur_token_id -= q_seq_len_local_.GetValue(i);
    }
    bool inc;
    GetIncrementalMode(i, &inc);
    if (inc) {
      int kv_seq;
      GetKVSeqLen(i, &kv_seq);
      *position_id = kv_seq - 1;
    }
  }
  __aicore__ inline void GetKVSeqId(int token_id, int *seq_id) {
    *seq_id = (kv_padding_offset_global_.GetValue(token_id) + token_id) % seq_len_;
  }
  __aicore__ inline void GetTokenIdByBatch(int batch_id, int *token_id) {
    *token_id = 0;
    for (size_t i = 0; i < batch_id; i++) {
      *token_id += q_seq_len_local_.GetValue(i);
    }
  }
  __aicore__ inline void GetIncrementalMode(int batch_id, bool *incremental) {
    *incremental = (mode_local_.GetValue(batch_id) > 0);
  }
  __aicore__ inline void GetActualOffset(int batch_id, int *offset) {
    *offset = 0;
    for (size_t i = 0; i < batch_id; i++) {
      *offset += (mode_local_.GetValue(i) > 0) ? 1 : seq_len_;
    }
  }
  __aicore__ inline void GetActualBatchAndToken(int *batch_id, int *token_id, int current_elem) {
    for (size_t i = 0; i < batch_; i++) {
      *token_id = current_elem;
      *batch_id = i;
      current_elem -= (mode_local_.GetValue(i) > 0) ? 1 : seq_len_;
      if (current_elem < 0) break;
    }
  }

 private:
  int batch_, max_token_, actual_token_, seq_len_;
  TPipe *pipe_;

  GlobalTensor<int> q_seq_len_global_;
  GlobalTensor<int> kv_seq_len_global_;
  GlobalTensor<int> q_padding_offset_global_;
  GlobalTensor<int> kv_padding_offset_global_;
  GlobalTensor<int> mode_global_;

  LocalTensor<int> q_seq_len_local_;
  LocalTensor<int> kv_seq_len_local_;
  LocalTensor<int> mode_local_;

  TBuf<QuePosition::VECIN> q_seq_len_local_ptr_;
  TBuf<QuePosition::VECIN> kv_seq_len_local_ptr_;
  TBuf<QuePosition::VECIN> q_padding_offset_local_ptr_;
  TBuf<QuePosition::VECIN> kv_padding_offset_local_ptr_;
  TBuf<QuePosition::VECIN> mode_local_ptr_;
};

class KernelVSLCreate {
 public:
  __aicore__ inline KernelVSLCreate() = default;
  __aicore__ inline uint32_t InitReduceWorkspaceSize() {
    constexpr int block_size = 32;
    constexpr int repeat_size = 256;
    int type_size = sizeof(float);
    // Number of elements a block can hold
    int elements_per_block = block_size / type_size;
    // Number of elements that can be processed in a repeat
    int elements_per_repeat = repeat_size / type_size;
    int first_max_repeat = UP_DIV(batch_size_, elements_per_repeat);
    int iter1_align_end = UP_DIV(first_max_repeat, elements_per_block) * elements_per_block;
    return iter1_align_end;
  }
  __aicore__ inline void Init(GM_ADDR batch_valid_len_gm, GM_ADDR position_idx_gm, GM_ADDR q_seq_len_gm,
                              GM_ADDR kv_seq_len_gm, GM_ADDR q_padding_offset_gm, GM_ADDR kv_padding_offset_gm,
                              GM_ADDR mode, GM_ADDR token_num_gm, GM_ADDR batch_to_batch_gm, uint32_t batch_size,
                              uint32_t max_seq_len) {
    max_seq_len_ = max_seq_len;
    batch_size_ = batch_size;
    is_mode_in_ = (position_idx_gm == nullptr);
    uint32_t reduce_work_space_size = InitReduceWorkspaceSize();
    batch_valid_len_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(batch_valid_len_gm), batch_size_);
    position_idx_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(position_idx_gm), batch_size * max_seq_len);
    q_seq_len_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(q_seq_len_gm), batch_size);
    kv_seq_len_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(kv_seq_len_gm), batch_size);
    q_padding_offset_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(q_padding_offset_gm),
                                             batch_size * max_seq_len);
    kv_padding_offset_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(kv_padding_offset_gm),
                                              batch_size * max_seq_len);
    mode_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(mode), batch_size);
    token_num_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(token_num_gm), 2);
    is_prompt_and_inc_ = (batch_to_batch_gm == nullptr) ? false : true;
    if (is_prompt_and_inc_) {
      batch_to_batch_global_.SetGlobalBuffer(reinterpret_cast<__gm__ int *>(batch_to_batch_gm), batch_size);
    }
    if (is_mode_in_) {
      pipe_.InitBuffer(reduce_tmp_, ALIGN32(reduce_work_space_size * sizeof(float)));
      pipe_.InitBuffer(reduce_output_tmp_, ALIGN32(1 * sizeof(float)));
      pipe_.InitBuffer(cast_mode_tmp_, ALIGN32(batch_size_ * sizeof(float)));
      reduce_tmp_local_ = reduce_tmp_.Get<float>();
      reduce_output_tmp_local_ = reduce_output_tmp_.Get<float>();
      cast_mode_tmp_local_ = cast_mode_tmp_.Get<float>();
      TBuf<QuePosition::VECCALC> mode_tmp;
      pipe_.InitBuffer(mode_tmp, ALIGN32(batch_size_ * sizeof(int)));
      LocalTensor<int> mode_tmp_local = mode_tmp.Get<int>();
      DataCopy(mode_tmp_local, mode_global_, ALIGN_BY_TYPE(batch_size_, sizeof(int), 32));
      pipe_barrier(PIPE_ALL);  // syncronize
      Cast(cast_mode_tmp_local_, mode_tmp_local, AscendC::RoundMode::CAST_NONE,
           ALIGN_BY_TYPE(batch_size_, sizeof(int), 32));
      pipe_barrier(PIPE_ALL);  // syncronize
    }
    pipe_.InitBuffer(q_tmp_, ALIGN32(max_seq_len * sizeof(int)));
    pipe_.InitBuffer(kv_tmp_, ALIGN32(max_seq_len * sizeof(int)));
    q_tmp_local_ = q_tmp_.Get<int>();
    kv_tmp_local_ = kv_tmp_.Get<int>();
  }

  __aicore__ inline void Process() {
    int prompt_count = 0;
    int inc_count = 0;
    if (is_prompt_and_inc_) {
      CreateBatchToBath(&prompt_count, &inc_count);
    } else {
      if (position_idx_global_.GetValue(0) > 0) {
        prompt_count = 0;
      } else {
        prompt_count = batch_size_;
      }
    }
    int q_total_seq_len = 0;
    int kv_total_seq_len = 0;
    int q_cum_offset = 0;
    int kv_cum_offset = 0;
    for (size_t batch_id = 0; batch_id < batch_size_; batch_id++) {
      int seq_pos = max_seq_len_;
      int real_batch_id = batch_id;
      if (is_prompt_and_inc_) {
        real_batch_id = batch_to_batch_global_.GetValue(batch_id);
      }
      int incremental = (batch_id >= prompt_count) ? 1 : 0;
      mode_global_.SetValue(batch_id, incremental);
      int token_num = batch_valid_len_global_.GetValue(real_batch_id);
      token_num = (token_num == -1) ? 0 : (is_mode_in_) ? token_num : token_num + 1;
      int q_token_num = (incremental && token_num != 0) ? 1 : token_num;
      q_seq_len_global_.SetValue(batch_id, q_token_num);
      kv_seq_len_global_.SetValue(batch_id, token_num);
      Muls(q_tmp_local_, q_tmp_local_, 0, ALIGN_BY_TYPE(q_token_num, sizeof(int), 32));
      Muls(kv_tmp_local_, kv_tmp_local_, 0, ALIGN_BY_TYPE(token_num, sizeof(int), 32));
      pipe_barrier(PIPE_ALL);
      Adds(q_tmp_local_, q_tmp_local_, q_cum_offset, ALIGN_BY_TYPE(q_token_num, sizeof(int), 32));
      Adds(kv_tmp_local_, kv_tmp_local_, kv_cum_offset, ALIGN_BY_TYPE(token_num, sizeof(int), 32));
      pipe_barrier(PIPE_ALL);
      DataCopy(q_padding_offset_global_[q_total_seq_len], q_tmp_local_, ALIGN_BY_TYPE(q_token_num, sizeof(int), 32));
      DataCopy(kv_padding_offset_global_[kv_total_seq_len], kv_tmp_local_, ALIGN_BY_TYPE(token_num, sizeof(int), 32));
      pipe_barrier(PIPE_ALL);
      q_cum_offset += max_seq_len_ - q_token_num;
      kv_cum_offset += max_seq_len_ - token_num;
      q_total_seq_len += q_token_num;
      kv_total_seq_len += token_num;
    }
    token_num_global_.SetValue(0, q_total_seq_len);
    token_num_global_.SetValue(1, kv_total_seq_len);
  }
  __aicore__ inline void CreateBatchToBath(int *prompt_count, int *inc_count) {
    int sum_inc;
    int sum_null = 0;
    for (size_t batch_id = 0; batch_id < batch_size_; batch_id++) {
      int incremental;
      if (!is_mode_in_) {
        int offset = (*prompt_count) * max_seq_len_ + (*inc_count);
        incremental = (position_idx_global_.GetValue(offset) > 0) ? 1 : 0;
      } else {
        incremental = ((int)cast_mode_tmp_local_.GetValue(batch_id) > 0) ? 1 : 0;
      }
      if (batch_valid_len_global_.GetValue(batch_id) == -1) {
        batch_to_batch_global_.SetValue(batch_size_ - 1 - sum_null++, batch_id);
      }
      if (!incremental && batch_valid_len_global_.GetValue(batch_id) != -1) {
        batch_to_batch_global_.SetValue((*prompt_count), batch_id);
        (*prompt_count)++;
      }
    }
    for (size_t batch_id = 0; batch_id < batch_size_; batch_id++) {
      int incremental;
      if (!is_mode_in_) {
        int offset = (*prompt_count) * max_seq_len_ + (*inc_count);
        incremental = (position_idx_global_.GetValue(offset) > 0) ? 1 : 0;
      } else {
        incremental = (mode_global_.GetValue(batch_id) > 0) ? 1 : 0;
      }
      if (incremental && batch_valid_len_global_.GetValue(batch_id) != -1) {
        batch_to_batch_global_.SetValue((*prompt_count) + (*inc_count), batch_id);
        (*inc_count)++;
      }
    }
  }

 private:
  GlobalTensor<int> batch_valid_len_global_;
  GlobalTensor<int> position_idx_global_;
  GlobalTensor<int> q_seq_len_global_;
  GlobalTensor<int> kv_seq_len_global_;
  GlobalTensor<int> q_padding_offset_global_;
  GlobalTensor<int> kv_padding_offset_global_;
  GlobalTensor<int> mode_global_;
  GlobalTensor<int> token_num_global_, batch_to_batch_global_;
  TBuf<QuePosition::VECCALC> q_tmp_;
  TBuf<QuePosition::VECCALC> kv_tmp_;
  TBuf<QuePosition::VECCALC> cast_mode_tmp_;
  TBuf<QuePosition::VECCALC> reduce_output_tmp_;
  TBuf<QuePosition::VECCALC> reduce_tmp_;
  LocalTensor<float> reduce_tmp_local_;
  LocalTensor<float> reduce_output_tmp_local_;
  LocalTensor<float> cast_mode_tmp_local_;

  LocalTensor<int> q_tmp_local_;
  LocalTensor<int> kv_tmp_local_;
  TPipe pipe_;
  uint32_t max_seq_len_, batch_size_;
  bool is_mode_in_;
  bool is_prompt_and_inc_;
};

__aicore__ void KernelCreateVSLOperator(GM_ADDR batch_valid_len_gm, GM_ADDR position_idx_gm, GM_ADDR q_seq_len_gm,
                                        GM_ADDR kv_seq_len_gm, GM_ADDR q_padding_offset_gm,
                                        GM_ADDR kv_padding_offset_gm, GM_ADDR mode_gm, GM_ADDR token_num_gm,
                                        GM_ADDR token_to_token_gm, uint32_t batch_size, uint32_t max_seq_len) {
  KernelVSLCreate op;
  op.Init(batch_valid_len_gm, position_idx_gm, q_seq_len_gm, kv_seq_len_gm, q_padding_offset_gm, kv_padding_offset_gm,
          mode_gm, token_num_gm, token_to_token_gm, batch_size, max_seq_len);
  op.Process();
}

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_VSL_UTILS_H_
