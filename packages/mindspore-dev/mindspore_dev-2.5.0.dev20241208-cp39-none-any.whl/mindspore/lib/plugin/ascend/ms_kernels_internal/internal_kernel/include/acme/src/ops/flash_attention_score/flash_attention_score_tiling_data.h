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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_FLASH_ATTENTION_SCORE_FLASH_ATTENTION_SCORE_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_FLASH_ATTENTION_SCORE_FLASH_ATTENTION_SCORE_TILING_H_

#include <cstdint>

#pragma pack(8)
typedef struct {
  uint64_t batch_size;
  uint64_t num_heads;
  uint64_t max_seqlen;
  uint64_t head_dim;
  uint64_t num_group;
  uint64_t q_seqlen;
  uint64_t kv_seqlen;
  uint64_t table_block_size;
  uint64_t sync_addr;
  uint64_t core_num;
  float tor;
} BSAttentionTilingData;
#pragma pack()

#ifndef __BS_ATTENTION_TILING_H__
#define __BS_ATTENTION_TILING_H__

#define MAX_CORE_NUM 25
#define ATTENTION_DEBUG false  // 开启时会对S/P写入调试数据
#define ROWMAX true
#define OP_NAME FlashAttentionScore
#define BUFFER_NUM 4  // 核间流水数，暂不支持修改

#if BFLOAT16
#define TYPE_NAME _bf16
#else
#define TYPE_NAME _fp16
#endif

#if BSH
#define LAYOUT_NAME _BSH
#else
#define LAYOUT_NAME _BNSD
#endif

#if LOWER_TRIANGLE
#define TRI_NAME _tri
#else
#define TRI_NAME _full
#endif

#define CONCAT_(A, B, C, D, E) A##B##C##D##E
#define CONCAT(A, B, C, D, E) CONCAT_(A, B, C, D, E)
#define FUNC_NAME_AIC CONCAT(OP_NAME, TYPE_NAME, LAYOUT_NAME, TRI_NAME, _mix_aic)
#define FUNC_NAME_AIV CONCAT(OP_NAME, TYPE_NAME, LAYOUT_NAME, TRI_NAME, _mix_aiv)

// **************mask patten模式**************//
// 第一种：下三角，开启LOWER_TRIANGLE时会直接采用下三角，不依赖mask
// #define LOWER_TRIANGLE false

// 第二种：Block Sparse，LOWER_TRIANGLE关闭时，开启BLOCK_SPARSE，会使用pre_token和next_token，不依赖mask（待开发）
// #define BLOCK_SPARSE false

// 第三种：读取MASK，LOWER_TRIANGLE和BLOCK_SPARSE关闭时，开启AMASK，会使用mask作为输入
// #define AMASK true

// 第四种：全矩阵，LOWER_TRIANGLE、BLOCK_SPARSE和AMASK如果全部关闭，则此attention采用全矩阵运算，不抑制S中的元素
// *******************************************//

constexpr uint64_t WORKSPACE_MAX_SEQLEN = 4096;
constexpr uint64_t MAX_ROW = 128;
constexpr uint64_t WORKSPACE_MAX_SEQLEN_BLOCK = WORKSPACE_MAX_SEQLEN / 16;
constexpr uint64_t WORKSPACE_SIZE0 = MAX_ROW * WORKSPACE_MAX_SEQLEN;  // for s, p
constexpr uint64_t WORKSPACE_SIZE1 = MAX_ROW * MAX_ROW;               // for o_tmp
constexpr uint64_t WORKSPACE_SIZE2 = MAX_ROW * MAX_ROW;               // for global_o

constexpr uint64_t WORKSPACE_OFFSET1 = WORKSPACE_SIZE0;
constexpr uint64_t WORKSPACE_OFFSET2 = WORKSPACE_OFFSET1 + WORKSPACE_SIZE1;
constexpr uint64_t WORKSPACE_SIZE = WORKSPACE_SIZE0 + WORKSPACE_SIZE1 + WORKSPACE_SIZE2;
constexpr uint64_t BUFFER_SIZE = WORKSPACE_SIZE * MAX_CORE_NUM * sizeof(uint16_t);
#endif  // end of __BS_ATTENTION_TILING_H__

#endif  //  MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_FLASH_ATTENTION_SCORE_FLASH_ATTENTION_SCORE_TILING_H_

