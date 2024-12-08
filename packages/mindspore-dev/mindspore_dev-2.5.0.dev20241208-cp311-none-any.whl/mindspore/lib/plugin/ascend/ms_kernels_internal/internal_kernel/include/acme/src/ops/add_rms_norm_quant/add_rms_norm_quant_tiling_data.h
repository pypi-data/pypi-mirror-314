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

#ifndef MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_ADD_RMS_NORM_QUANT_TILING_H_
#define MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_ADD_RMS_NORM_QUANT_TILING_H_

#include <cstdint>

#pragma pack(1)

struct AddRmsNormQuantTilingData {
  uint32_t num_row = 0;
  uint32_t num_col = 0;
  uint32_t block_factor = 0;
  uint32_t row_factor = 0;
  uint32_t ub_factor = 0;
  float epsilon = 0;
  float avg_factor = 0;
  bool has_zeropoints1 = true;
  uint32_t tiling_key = 0;
  bool is_broadcast = false;
};

#pragma pack()

#endif  // MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_ADD_RMS_NORM_QUANT_TILING_H_
