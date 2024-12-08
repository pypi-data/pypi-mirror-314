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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_PP_MATMUL_INFO_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_PP_MATMUL_INFO_H_

#include <array>
#include <map>
#include <iostream>

namespace mindspore {
namespace acme {
namespace tiling {
struct MatMulInfo {
  uint32_t batchSize{0};
  uint32_t m{0};       // 实际输入的 m
  uint32_t n{0};       // 实际输入的 n
  uint32_t k{0};       // 实际输入的 k
  bool transA{0};      // false: 0, true: 1
  bool transB{0};      // false: 0, true: 1
  bool formatSema{0};  // "FRACTAL_NZ": 0, "ND": 1
  bool biasFlag{0};    // false: 0, true: 1
  bool isInt8{0};      // 是否shi int8融合
  float inDtype{0};
  float outDtype{0};
};

struct OpShape {
  uint32_t batchSize{0};
  uint32_t m{0};
  uint32_t k{0};
  uint32_t n{0};
  uint32_t m0{0};
  uint32_t k0{0};
  uint32_t n0{0};
};

struct PpTilingData {
  OpShape opShape{};
  uint32_t mLoop{1};
  uint32_t kLoop{1};
  uint32_t nLoop{1};
  uint32_t coreLoop{1};
  uint32_t swizzleCount{1};
  uint32_t tilingKey{0};
  uint32_t blockDim{1};
  uint32_t swizzleDirect{0};
  uint32_t splitk{0};

  void SetBaseShape(uint32_t batchSize, uint32_t m, uint32_t k, uint32_t n);
  void SetBaseOp(uint32_t coreNum, uint32_t mBase, uint32_t nBase, bool isInt8);
  void SetTilingKey(const MatMulInfo &mmInfo, uint32_t swizzleDirect, uint32_t enSplitK);
  uint32_t End(const MatMulInfo &mmInfo);
};
}  // namespace tiling
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_PP_MATMUL_INFO_H_