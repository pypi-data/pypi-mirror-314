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

#ifndef MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_CAST_CAST_TILING_H_
#define MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_CAST_CAST_TILING_H_

#include <cstdint>

namespace mindspore {
namespace acme {
enum CastDType : int32_t {
  FLOAT16_TO_FLOAT = 17,
  FLOAT16_TO_UINT8,
  FLOAT16_TO_INT8,
  FLOAT16_TO_INT16,
  FLOAT16_TO_INT32,
  FLOAT16_TO_BF16,

  FLOAT_TO_FLOAT16 = 33,
  FLOAT_TO_UINT8,
  FLOAT_TO_INT8,
  FLOAT_TO_INT32,
  FLOAT_TO_BF16,

  INT8_TO_FLOAT16 = 48,
  INT8_TO_FLOAT,
  INT8_TO_BF16,

  INT32_TO_INT64 = 99,
  INT32_TO_FLOAT,

  INT64_TO_INT32 = 114,
  INT64_TO_FLOAT,

  BF16_TO_FLOAT16 = 147,
  BF16_TO_FLOAT,

  UNSUPPORTED_DTYPE
};

typedef struct CastTilingData {
  uint32_t buffer_num;
  uint32_t cast_dtype;
  uint32_t core_num;

  uint32_t avg_block_count;
  uint32_t avg_block_ub_num;
  uint32_t avg_block_ub_tail;
  uint32_t avg_block_ub_loop;

  uint32_t tail_block_count;
  uint32_t tail_block_ub_num;
  uint32_t tail_block_ub_tail;
  uint32_t tail_block_ub_loop;
} CastTilingData;
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_CAST_CAST_TILING_H_
