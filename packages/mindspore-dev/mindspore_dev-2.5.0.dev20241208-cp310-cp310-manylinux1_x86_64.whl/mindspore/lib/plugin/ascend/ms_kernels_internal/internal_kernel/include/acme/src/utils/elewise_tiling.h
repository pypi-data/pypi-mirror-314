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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ELEWISE_TILINT_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ELEWISE_TILINT_H_

#include <stdint.h>
namespace mindspore {
namespace acme {
enum BroadcastMode : uint32_t {
  BROADCAST_NONE = 0,     /* in1 == in2 */
  BROADCAST_LEFT,         /* in1 != in2  && in2 == out */
  BROADCAST_RIGHT,        /* in1 != in2  && in1 == out */
  BROADCAST_SCALAR_LEFT,  /* in1 != in2  && in1 == 1 */
  BROADCAST_SCALAR_RIGHT, /* in1 != in2  && in2 == 1 */
  BROADCAST_BOTH,         /* in1 != in2  && in1 != out && in2 != out */
  UNKNOW_BROADCAST_MODE
};
struct ElewiseTailTilingData {
  uint32_t avg_block_count{0};
  uint32_t avg_block_ub_num{0};
  uint32_t avg_block_ub_tail{0};
  uint32_t avg_block_ub_loop{0};

  uint32_t tail_block_count{0};
  uint32_t tail_block_ub_num{0};
  uint32_t tail_block_ub_tail{0};
  uint32_t tail_block_ub_loop{0};

  uint32_t buffer_num{1};
  uint32_t block_dim{1};
};
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ELEWISE_TILINT_H_
