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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_TILING_DATA_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_TILING_DATA_H_

#include <stdint.h>

namespace mindspore {
namespace acme {
namespace tiling {
struct MsMatmulTilingData {
  // commom
  uint32_t batch{0};
  uint32_t m{0};
  uint32_t k{0};
  uint32_t n{0};
  uint32_t m0{0};
  uint32_t k0{0};
  uint32_t n0{0};
  uint32_t mLoop{0};
  uint32_t kLoop{0};
  uint32_t nLoop{0};
  uint32_t coreLoop{0};
  uint32_t blockDim{1};
  uint32_t swizzleCount{0};
  uint32_t swizzleDirect{0};
  uint32_t enShuffleK{0};
  uint64_t syncAddr{0};
  uint32_t tilingId{0};
  uint32_t tilingKey{0};
  // custom
  uint32_t blockDimM{0};
  uint32_t blockDimN{0};
  uint32_t blockLenM{0};
  uint32_t blockLenN{0};
  uint32_t mmadK{0};
};

struct MultiWeightMatmulTilingData {
  // commom
  uint32_t batch{0};
  uint32_t m{0};
  uint32_t k{0};
  uint32_t n{0};
  uint32_t m0{0};
  uint32_t k0{0};
  uint32_t n0{0};
  uint32_t mLoop{0};
  uint32_t kLoop{0};
  uint32_t nLoop{0};
  uint32_t coreLoop{0};
  uint32_t blockDim{1};
  uint32_t swizzleCount{0};
  uint32_t swizzleDirect{0};
  uint32_t enShuffleK{0};
  uint32_t mm_n_len_0{0};
  uint32_t mm_n_len_1{0};
  uint32_t mm_n_len_2{0};
  uint64_t syncAddr{0};
  uint32_t siluPos{0};
  uint32_t tilingId{0};
  uint32_t tilingKey{0};

  // custom
  uint32_t blockDimM{0};
  uint32_t blockDimN{0};
  uint32_t blockLenM{0};
  uint32_t blockLenN{0};
  uint32_t mmadK{0};
};
constexpr size_t maxTilingBufSize = sizeof(uint32_t) * 32;

}  // namespace tiling
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_TILING_DATA_H_