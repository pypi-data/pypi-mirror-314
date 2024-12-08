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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_RESHAPE_AND_CACHE_NZ_RESHAPE_AND_CACHE_NZ_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_RESHAPE_AND_CACHE_NZ_RESHAPE_AND_CACHE_NZ_TILING_H_

#include <cstdint>
#include <sstream>
#include "acme/include/base_type.h"

namespace mindspore::acme {
#pragma pack(1)
struct AcmeReshapeAndCacheNzTilingData {
  int32_t num_tokens;
  int32_t hidden_size;
  int32_t dtype_size;
  int32_t block_size;
};
#pragma pack()

static std::ostringstream &operator<<(std::ostringstream &os, const AcmeReshapeAndCacheNzTilingData &dt) {
  os << "ReshapeAndCacheNz Tiling: ";
  os << "num_tokens:" << dt.num_tokens;
  os << ", hidden_size:" << dt.hidden_size;
  os << ", dtype_size:" << dt.dtype_size;
  os << ", block_size:" << dt.block_size;
  return os;
}

AcmeStatus ReshapeAndCacheNzTilingImpl(RawHostAddr &host_ptr, const InputsDescList &inputs, uint32_t *block_dims);
}  // namespace mindspore::acme

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_RESHAPE_AND_CACHE_NZ_RESHAPE_AND_CACHE_NZ_TILING_H_