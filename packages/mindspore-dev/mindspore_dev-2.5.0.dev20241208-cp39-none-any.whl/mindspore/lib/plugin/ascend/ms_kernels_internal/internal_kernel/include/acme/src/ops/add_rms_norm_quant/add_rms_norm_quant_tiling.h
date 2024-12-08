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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_ADD_RMS_NORM_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_ADD_RMS_NORM_TILING_H_

#include "add_rms_norm_quant_tiling_data.h"
#include "acme/include/base_type.h"
#include <sstream>

namespace mindspore {
namespace acme {

static std::ostringstream &operator<<(std::ostringstream &os, const AddRmsNormQuantTilingData &dt) {
  os << "AddRmsNormQuant Tiling: ";
  os << "num_row:" << dt.num_row;
  os << ", num_col:" << dt.num_col;
  os << ", block_factor:" << dt.block_factor;
  os << ", row_factor:" << dt.row_factor;
  os << ", ub_factor:" << dt.ub_factor;
  os << ", epsilon:" << dt.epsilon;
  os << ", avg_factor:" << dt.avg_factor;
  os << ", has_zeropoints1:" << dt.has_zeropoints1;
  os << ", tiling_key:" << dt.tiling_key;
  os << ", is_broadcast:" << dt.is_broadcast;

  return os;
};

void AddRmsNormQuantTilingImpl(RawHostAddr host_ptr, const float eps, const int64_t num_row, const int64_t num_col,
                               const DataType tensor_dtype, uint32_t &max_core_num, bool is_broadcast);
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_ADD_RMS_NORM_TILING_H_