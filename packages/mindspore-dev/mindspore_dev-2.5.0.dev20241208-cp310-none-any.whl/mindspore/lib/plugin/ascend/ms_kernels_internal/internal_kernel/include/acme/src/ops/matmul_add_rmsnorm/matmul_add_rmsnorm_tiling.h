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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_ADD_RMSNORM_MATMUL_ADD_RMSNORM_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_ADD_RMSNORM_MATMUL_ADD_RMSNORM_TILING_H_

#include <stdint.h>
#include <sstream>
#include "acme/src/ops/matmul_common/pp_matmul_common_tiling.h"
#include "acme/include/base_type.h"
#include <unordered_map>

using namespace mindspore::acme::tiling;
using namespace mindspore::acme;

static uint32_t MatmulAddRmsNormSwizzle(PpTilingData &tilingData) {
  uint32_t swizzleDirect = 0;
  uint32_t swizzleCount = 1;
  float m0 = tilingData.opShape.m0;
  float n0 = tilingData.opShape.n0;
  float m = tilingData.opShape.m;
  float k = tilingData.opShape.k;
  float n = tilingData.opShape.n;
  float mincost = m * k + k * n;

  for (uint32_t i = 1; i <= tilingData.blockDim; ++i) {
    int c = static_cast<int32_t>((tilingData.blockDim + i - 1) / i);
    float cost;
    // Matmul-Add-RmsNorm swizzle direction is affected by the rmsnorm op
    swizzleDirect = 0;  // Zn
    cost = m0 * i + n0 * c;
    if (cost < mincost) {
      mincost = cost;
      swizzleCount = i;
    }
  }
  tilingData.swizzleDirect = swizzleDirect;
  tilingData.swizzleCount = swizzleCount;
  return swizzleDirect;
}

struct MatmulAddRmsNormTilingData {
  uint32_t tilingId{0};
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
  uint32_t swizzleCount{0};
  uint32_t tilingKey{0};
  uint32_t blockDim{1};
  uint32_t swizzleDirect{0};
  uint32_t splitk{0};
  float eps{0.0f};

  std::string TilingDataDump() {
    std::ostringstream oss;
    oss << "tilingId = " << tilingId << std::endl;
    oss << "batch = " << batch << std::endl;
    oss << "m = " << m << std::endl;
    oss << "k = " << k << std::endl;
    oss << "n = " << n << std::endl;
    oss << "m0 = " << m0 << std::endl;
    oss << "k0 = " << k0 << std::endl;
    oss << "n0 = " << n0 << std::endl;
    oss << "mLoop = " << mLoop << std::endl;
    oss << "kLoop = " << kLoop << std::endl;
    oss << "nLoop = " << nLoop << std::endl;
    oss << "coreLoop = " << coreLoop << std::endl;
    oss << "swizzleCount = " << swizzleCount << std::endl;
    oss << "tilingKey = " << tilingKey << std::endl;
    oss << "blockDim = " << blockDim << std::endl;
    oss << "swizzleDirect = " << swizzleDirect << std::endl;
    oss << "splitk = " << splitk << std::endl;
    oss << "eps = " << eps << std::endl;
    return oss.str();
  }

  void Tiling(const MatmulAddRmsNormParam &param, uint32_t mm, uint32_t kk, uint32_t nn, DataType MatmulDType,
              DataType RmsNormDType, const HardwareConfig &hw_info, uint32_t tiling_id) {
    std::unordered_map<DataType, float> dTypeMap = {{DataType::kTypeInt8, 1.0},
                                                    {DataType::kTypeFloat16, 2.0},
                                                    {DataType::kTypeBF16, 2.0},
                                                    {DataType::kTypeFloat32, 4.0}};
    MatMulInfo mmInfo;
    mmInfo.batchSize = 1;
    mmInfo.m = mm;
    mmInfo.k = kk;
    mmInfo.n = nn;
    mmInfo.transA = param.transpose_a;
    mmInfo.transB = param.transpose_b;
    mmInfo.isInt8 = false;
    mmInfo.inDtype = dTypeMap[MatmulDType];
    mmInfo.outDtype = dTypeMap[RmsNormDType];
    mmInfo.biasFlag = 0;

    OpShape opShape;
    opShape.batchSize = mmInfo.batchSize;
    opShape.m = mmInfo.m;
    opShape.n = mmInfo.n;
    opShape.k = mmInfo.k;

    PpTilingData pptilingdata;
    pptilingdata.opShape = opShape;
    pptilingdata.SetTilingKey(mmInfo, 0, 0);

    if (opShape.m < opShape.n) {
      TilingFunc<false, OpShape, PpTilingData, HardwareConfig, MatMulInfo>(opShape, pptilingdata, hw_info, mmInfo);
    } else {
      TilingFunc<true, OpShape, PpTilingData, HardwareConfig, MatMulInfo>(opShape, pptilingdata, hw_info, mmInfo);
    }

    uint32_t direct = MatmulAddRmsNormSwizzle(pptilingdata);
    blockDim = pptilingdata.End(mmInfo);
    pptilingdata.SetTilingKey(mmInfo, direct, 0);

    tilingId = tiling_id;
    batch = pptilingdata.opShape.batchSize;
    m = pptilingdata.opShape.m;
    k = pptilingdata.opShape.k;
    n = pptilingdata.opShape.n;
    m0 = pptilingdata.opShape.m0;
    k0 = pptilingdata.opShape.k0;
    n0 = pptilingdata.opShape.n0;
    mLoop = pptilingdata.mLoop;
    kLoop = pptilingdata.kLoop;
    nLoop = pptilingdata.nLoop;
    coreLoop = pptilingdata.coreLoop;
    swizzleCount = pptilingdata.swizzleCount;
    tilingKey = pptilingdata.tilingKey;
    swizzleDirect = pptilingdata.swizzleDirect;
    splitk = 0;
    eps = param.eps;
  }
};

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_ADD_RMSNORM_MATMUL_ADD_RMSNORM_TILING_H_
