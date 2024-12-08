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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_LAYER_NORM_ADD_LAYER_NORM_TILING_DATA_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_LAYER_NORM_ADD_LAYER_NORM_TILING_DATA_H_

#include <cstdint>

#pragma pack(1)

struct AddLayerNormTilingData {
  uint32_t numCore = 0;
  uint32_t numLastDim = 0;
  uint32_t numFirstDim = 0;
  uint32_t firstDimPerCore = 0;
  uint32_t firstDimPerCoreTail = 0;
  uint32_t firstDimPerTime = 0;
  uint32_t lastDimPerTime = 0;
  float eps = 0;
  float aveFactor = 0;
  uint32_t colMoveCnt = 0;
  uint32_t colTail = 0;
  uint32_t workspaceSize = 0;
  uint32_t tiling_key = 0;
  uint32_t data_type = 0;
};

#pragma pack()

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_LAYER_NORM_ADD_LAYER_NORM_TILING_DATA_H_