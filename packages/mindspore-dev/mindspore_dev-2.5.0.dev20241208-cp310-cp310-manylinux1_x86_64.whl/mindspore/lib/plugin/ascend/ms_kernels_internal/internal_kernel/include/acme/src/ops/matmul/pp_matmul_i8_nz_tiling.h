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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_310P_PP_MATMUL_I8_NZ_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_310P_PP_MATMUL_I8_NZ_TILING_H_

#include <array>
#include <map>
#include <iostream>
#include "acme/src/core/platform/platform_configs.h"

namespace mindspore {
namespace acme {
namespace tiling {
constexpr uint32_t PP_MATMUL_TILING_SIZE = 512;
constexpr uint32_t NUM_TILING_FIELD = 12;
// constexpr uint32_t RESERVED_SIZE = 512 - sizeof(OpShape310P) - sizeof(int32_t) * 9;

struct MatMulInfo310P {
    uint32_t batchSize{0};
    uint32_t m{0};  // 实际输入的 m
    uint32_t n{0};  // 实际输入的 n
    uint32_t k{0};  // 实际输入的 k
    uint32_t mCrop{0};
    uint32_t nCrop{0};
    bool transA{0};   // false: 0, true: 1
    bool transB{0};   // false: 0, true: 1
    bool biasFlag{0}; // false: 0, true: 1
    bool isInt8{0};   // 是否 int8融合
    bool isCompress{0};  // 是否compress
    uint32_t tilingK{0};
    uint32_t tilingN{0};
    float inDtype{2};
    float outDtype{4};
};

struct OpShape310P {
    uint32_t batchSize{0};
    uint32_t m{0};
    uint32_t k{0};
    uint32_t n{0};
    uint32_t m0{0};
    uint32_t k0{0};
    uint32_t n0{0};
};

struct PpTilingData310P {
    OpShape310P opShape{};
    uint32_t mLoop{1};
    uint32_t kLoop{1};
    uint32_t nLoop{1};
    uint32_t coreLoop{1};
    uint32_t swizzlCount{1};
    uint32_t tilingK{0};
    uint32_t tilingN{0};
    uint32_t compressOverlapN{0};
    uint32_t tilingKey{0};
    uint32_t blockDim{1};
    uint32_t swizzlDirect{0};
    uint32_t splitK{0};
    uint8_t reserved[PP_MATMUL_TILING_SIZE - sizeof(OpShape310P) - sizeof(int32_t) * NUM_TILING_FIELD];
    void SetBaseShape(uint32_t batchSize, uint32_t m, uint32_t k, uint32_t n);
    void SetBaseOp(uint32_t coreNum, uint32_t mBase, uint32_t nBase);
    void SetTilingKey(const MatMulInfo310P &mmInfo);
    uint32_t End(const MatMulInfo310P &mmInfo);
};
void GetPpTiling(const MatMulInfo310P &mmInfo, const HardwareConfig &hwInfo, uint32_t &blockDim,
                PpTilingData310P &tilingData);
} // namespace tiling
} // namespace acme
} // namespace mindspore

#endif // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_310P_PP_MATMUL_I8_NZ_TILING_H_
