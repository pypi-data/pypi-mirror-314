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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_LAYER_NORM_ADD_LAYER_NORM_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_LAYER_NORM_ADD_LAYER_NORM_TILING_H_

#include <cstdint>
#include <sstream>

#include "add_layer_norm_tiling_data.h"
#include "acme/include/base_type.h"

namespace mindspore {
namespace acme {

static std::ostringstream &operator<<(std::ostringstream &os, const AddLayerNormTilingData &dt) {
  os << "AddLayerNorm Tiling: ";
  os << "numCore:" << dt.numCore;
  os << ", numLastDim:" << dt.numLastDim;
  os << ", numFirstDim:" << dt.numFirstDim;
  os << ", firstDimPerCore:" << dt.firstDimPerCore;
  os << ", firstDimPerCoreTail:" << dt.firstDimPerCoreTail;
  os << ", firstDimPerTime:" << dt.firstDimPerTime;
  os << ", lastDimPerTime:" << dt.lastDimPerTime;
  os << ", eps:" << dt.eps;
  os << ", aveFactor:" << dt.aveFactor;
  os << ", data_type:" << dt.data_type;
  os << ", colTail:" << dt.colTail;
  os << ", workspaceSize:" << dt.workspaceSize;
  os << ", tiling_key:" << dt.tiling_key;
  return os;
}

void Tiling4AddLayerNorm(RawHostAddr host_ptr, const InputsDescList &inputs, const float eps, uint32_t &maxCoreNum,
                         bool is310P, uint64_t maxUbSize);
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_LAYER_NORM_ADD_LAYER_NORM_TILING_H_