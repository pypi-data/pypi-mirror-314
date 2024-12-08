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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_PAGED_ATTENTION_PAGED_ATTENTION_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_PAGED_ATTENTION_PAGED_ATTENTION_TILING_H_

#include <cstdint>

#pragma pack(8)
typedef struct {
  int8_t eye[1024];
  uint64_t type;
  uint64_t p1_type;
  uint64_t layout;
  uint64_t batch_size;
  uint64_t num_heads;
  uint64_t max_seqlen;
  uint64_t anti_max_batch_size;
  uint64_t anti_max_seqlen;
  uint64_t head_dim;
  uint64_t num_group;
  uint64_t q_seqlen;
  uint64_t table_block_size;
  uint64_t quant_mode;
  uint64_t quant_method;
  uint64_t is_score_out;
  uint64_t sync_addr;
  uint64_t core_num;
  float tor;
} PagedAttentionTilingData;
#pragma pack()

#ifndef __BS_ATTENTION_TILING_H__
#define __BS_ATTENTION_TILING_H__

#define MAX_CORE_NUM 25
#define ATTENTION_DEBUG 0  // 开启时会对S/P写入调试数据
#define ROWMAX true
#define OP_NAME PagedAttention
#define BUFFER_NUM 4  // 核间流水数，暂不支持修改

constexpr uint64_t WORKSPACE_MAX_SEQLEN = 16384;
constexpr uint64_t MAX_ROW = 128;
constexpr uint64_t WORKSPACE_MAX_SEQLEN_BLOCK = WORKSPACE_MAX_SEQLEN / 16;
constexpr uint64_t MAX_BN_NUM = 128;
constexpr uint64_t WORKSPACE_SIZE0 = 64 * WORKSPACE_MAX_SEQLEN;          // for s, p
constexpr uint64_t WORKSPACE_SIZE1 = MAX_BN_NUM * MAX_ROW * MAX_ROW;     // for o_tmp
constexpr uint64_t WORKSPACE_SIZE2 = MAX_BN_NUM * MAX_ROW;               // for softmax_max
constexpr uint64_t WORKSPACE_SIZE3 = MAX_BN_NUM * MAX_ROW;               // for softmax_sum
constexpr uint64_t WORKSPACE_SIZE4 = MAX_BN_NUM * WORKSPACE_MAX_SEQLEN;  // for quant k/v

constexpr uint64_t WORKSPACE_OFFSET1 = WORKSPACE_SIZE0;
constexpr uint64_t WORKSPACE_OFFSET2 = WORKSPACE_OFFSET1 + WORKSPACE_SIZE1;
constexpr uint64_t WORKSPACE_OFFSET3 = WORKSPACE_OFFSET2 + WORKSPACE_SIZE2;
constexpr uint64_t WORKSPACE_OFFSET4 = WORKSPACE_OFFSET3 + WORKSPACE_SIZE3;
constexpr uint64_t WORKSPACE_SIZE = WORKSPACE_SIZE0 + WORKSPACE_SIZE1 + WORKSPACE_SIZE2 + WORKSPACE_SIZE3 + WORKSPACE_SIZE4;
constexpr uint64_t BUFFER_SIZE = WORKSPACE_SIZE * MAX_CORE_NUM * sizeof(uint16_t);
#endif  // end of __BS_ATTENTION_TILING_H__

#endif  //  MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_PAGED_ATTENTION_PAGED_ATTENTION_TILING_H_