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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMPARE_COMPARE_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMPARE_COMPARE_TILING_H_

#include <sstream>
#include "acme/include/base_type.h"
#include "compare_tiling_data.h"
#include "acme/src/utils/elewise_tiling.h"

namespace mindspore {
namespace acme {

static std::ostringstream &operator<<(std::ostringstream &os, const ElewiseTailTilingData &dt) {
  os << ", avg_block_count:" << dt.avg_block_count;
  os << ", avg_block_ub_num:" << dt.avg_block_ub_num;
  os << ", avg_block_ub_tail:" << dt.avg_block_ub_tail;
  os << ", avg_block_ub_loop:" << dt.avg_block_ub_loop;
  os << ", tail_block_count:" << dt.tail_block_count;
  os << ", tail_block_ub_num:" << dt.tail_block_ub_num;
  os << ", tail_block_ub_tail:" << dt.tail_block_ub_tail;
  os << ", tail_block_ub_loop:" << dt.tail_block_ub_loop;
  os << ", buffer_num:" << dt.buffer_num;
  os << ", block_dim:" << dt.block_dim;
  return os;
}

static std::ostringstream &operator<<(std::ostringstream &os, const AcmeCompareTilingData &dt) {
  os << ", tiling_key:" << dt.tiling_key;
  os << ", broadcast_mode:" << dt.broadcast_mode;
  os << ", compare_mode:" << dt.compare_mode;
  ElewiseTailTilingData *ele_tiling = (ElewiseTailTilingData *)&dt;
  os << *ele_tiling;
  return os;
}

AcmeStatus CompareTilingImpl(const InputsDescList &inputs, const OutputsDescList &outputs, const uint32_t compare_mode, uint32_t *broadcast_mode_ptr, RawHostAddr &host_ptr);

}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMPARE_COMPARE_TILING_H_
