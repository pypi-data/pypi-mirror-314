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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_310P_COMMMON_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_310P_COMMMON_TILING_H_

#include <cmath>
#include "acme/src/core/platform/rt_funcs.h"
#include "acme/src/utils/comm_utils.h"

namespace mindspore {
namespace acme {
namespace tiling {
constexpr uint32_t FP16_SIZE = 2;
constexpr uint32_t FP32_SIZE = 4;
constexpr uint32_t BLOCK_SIZE = 16;
constexpr uint32_t BLOCK_SIZE_INT8_K = 32;
constexpr uint32_t BASE_BLOCK_STEP = 2;
constexpr uint32_t AXES_ALIGN_SIZE = 512;
constexpr uint32_t AXES_ALIGN_SIZE_INT8 = 256;
constexpr uint32_t ND_SHAPE_SIZE = 2;
constexpr uint32_t NZ_SHAPE_SIZE = 4;
constexpr uint32_t CUBE_BLOCK_SIZE = 256;
constexpr uint32_t CUBE_BLOCK_SIZE_INT8 = 512;
constexpr uint32_t L1AB_PINGPONG_BUFFER_LEN = 262144;
constexpr uint32_t L0AB_PINGPONG_BUFFER_LEN_INT8 = 131072 * 2;  // 256 KB
constexpr uint32_t L0AB_PINGPONG_BUFFER_LEN_FP16 = 131072;      // 128 KB
constexpr uint32_t L1AB_PINGPONG_BUFFER_LEN_INT8_SPARSE = 160 * 1024;

template <uint32_t DIV>
inline __attribute__((always_inline)) uint32_t CeilDiv(uint32_t num) {
  if (DIV == 0) {
    return 0;
  }
  return (num + DIV - 1) / DIV;
}

inline __attribute__((always_inline)) uint32_t CeilDiv(uint32_t dividend, uint32_t divisor) {
  if (divisor == 0) {
    return 0;
  }
  return (dividend + divisor - 1) / divisor;
}

template <uint32_t RND>
inline __attribute__((always_inline)) uint32_t Round(uint32_t num) {
  if (RND == 0) {
    return 0;
  }
  return (num + RND - 1) / RND * RND;
}

inline __attribute__((always_inline)) uint32_t RoundUp(uint32_t num, uint32_t rnd) {
  if (rnd == 0) {
    return 0;
  }
  return (num + rnd - 1) / rnd * rnd;
}

inline __attribute__((always_inline)) uint32_t RoundDown(uint32_t num, uint32_t rnd) {
  if (rnd == 0) {
    return 0;
  }
  return num / rnd * rnd;
}

template <typename HardwareType, typename OpShapeType>
inline __attribute__((always_inline)) float CostFunc(const HardwareType &hwInfor, OpShapeType &shape) {
  float aCoef = 1;
  float bCoef = 1;
  float bwCoef = static_cast<float>(hwInfor.l2_bandwidth_) / static_cast<float>(hwInfor.hbm_bandwidth_);
  uint32_t mLoop = CeilDiv(shape.m, shape.m0);
  uint32_t nLoop = CeilDiv(shape.n, shape.n0);
  if (mLoop == 0 || nLoop == 0) {
    return 1;
  }
  uint32_t coreNeed = shape.batchSize * mLoop * nLoop;
  uint32_t blockDim = std::min(coreNeed, hwInfor.core_num_);
  uint32_t mOnce = blockDim < nLoop ? shape.m0 : blockDim / nLoop * shape.m0;
  uint32_t nOnce = blockDim < nLoop ? hwInfor.core_num_ * shape.n0 : shape.n;
  if (mOnce * shape.k * FP16_SIZE > hwInfor.l2_size_) {
    aCoef = bwCoef;
  }
  if (nOnce * shape.k * FP16_SIZE > hwInfor.l2_size_) {
    bCoef = bwCoef;
  }
  return 1 / (aCoef * static_cast<float>(shape.n0)) + 1 / (bCoef * static_cast<float>(shape.m0));
}

template <bool PRI_FLAG, typename OpShareType, typename TilingType, typename HardwareType, typename MatMulInfoType>
void TilingFunc(OpShareType &opShape, TilingType &tilingParam, const HardwareType &hwInfor,
                const MatMulInfoType &mmInfo, bool compressFlag = false, const uint32_t tilingN = 1) {
  using namespace std;
  float costMin = 1;
  const float CONST_2 = 2.0;
  const uint32_t CONST_16 = 16;
  uint32_t roundBase =
    static_cast<uint32_t>(pow(2, ceil(log(CeilDiv(PRI_FLAG ? opShape.n : opShape.m, CONST_16)))) * CONST_16);
  uint32_t priAxes = RoundUp(PRI_FLAG ? opShape.m : opShape.n, CONST_16);
  uint32_t axes = RoundUp(PRI_FLAG ? opShape.n : opShape.m, roundBase);
  float axes0Max = static_cast<float>(AXES_ALIGN_SIZE) / mmInfo.inDtype;
  std::string soc_name_ = RtFuncs::GetInstance().GetSocVersion();  // TODO
  if (mmInfo.isInt8 && soc_name_.find("Ascend310P") != std::string::npos) {
    axes0Max /= CONST_2;
  }

  MSOP_LOG(INFO) << "hwInfor.l0c_size_ = " << hwInfor.l0c_size_;

  uint32_t n0TilingInit =
    compressFlag ? ((tilingN * BLOCK_SIZE > opShape.n) ? Round<16>(opShape.n) : tilingN * BLOCK_SIZE) : BLOCK_SIZE;

  uint32_t n0TilingLimit = compressFlag ? std::min(tilingN * BLOCK_SIZE, AXES_ALIGN_SIZE_INT8)  // TODO
                           : (soc_name_.find("Ascend310P") != std::string::npos) ? AXES_ALIGN_SIZE
                                                                                 : AXES_ALIGN_SIZE_INT8;

  MSOP_LOG(INFO) << "n0TilingLimit = " << n0TilingLimit << " tilingN size=" << tilingN * BLOCK_SIZE;
  uint32_t priAxes0Init = PRI_FLAG ? BLOCK_SIZE : n0TilingInit;
  uint32_t axes0Init = PRI_FLAG ? n0TilingInit : BLOCK_SIZE;

  for (uint32_t priAxes0 = priAxes0Init; priAxes0 <= priAxes && priAxes0 <= axes0Max; priAxes0 *= BASE_BLOCK_STEP) {
    for (uint32_t axes0 = axes0Init; axes0 <= axes && axes0 <= axes0Max; axes0 *= BASE_BLOCK_STEP) {
      if (priAxes0 * axes0 * FP32_SIZE > hwInfor.l0c_size_) {
        continue;
      }
      if (mmInfo.isInt8) {
        if (PRI_FLAG) {
          if (axes0 > n0TilingLimit) {
            continue;
          }
        } else {
          if (priAxes0 > n0TilingLimit) {
            continue;
          }
        }
      }
      opShape.m0 = PRI_FLAG ? priAxes0 : axes0;
      opShape.n0 = PRI_FLAG ? axes0 : priAxes0;
      float cost = CostFunc<HardwareType, OpShareType>(hwInfor, opShape);
      if (cost < costMin) {
        costMin = cost;
        if constexpr (std::is_same<TilingType, PpTilingData>::value) {
          tilingParam.SetBaseOp(hwInfor.core_num_, opShape.m0, opShape.n0, mmInfo.isInt8);
        } else {
          tilingParam.SetBaseOp(hwInfor.core_num_, opShape.m0, opShape.n0);
        }
      }
    }
  }
}

template <typename PpTilingDataType>
uint32_t Swizzl(PpTilingDataType &tilingData) {
  uint32_t swizzlDirect = 0;
  uint32_t swizzlCount = 1;
  float m0 = tilingData.opShape.m0;
  float n0 = tilingData.opShape.n0;
  float m = tilingData.opShape.m;
  float k = tilingData.opShape.k;
  float n = tilingData.opShape.n;
  float mincost = m * k + k * n;

  for (uint32_t i = 1; i <= tilingData.blockDim; ++i) {
    int c = static_cast<int32_t>((tilingData.blockDim + i - 1) / i);
    float cost;
    // B0 + A < A0 + B
    if (i * n0 + m < m0 * c + n) {
      swizzlDirect = 1;  // Nz
      cost = n0 * i + m0 * c;
      if (cost <= mincost) {
        mincost = cost;
        swizzlCount = i;
      }
    } else {
      swizzlDirect = 0;  // Zn
      cost = m0 * i + n0 * c;
      if (cost < mincost) {
        mincost = cost;
        swizzlCount = i;
      }
    }
  }
  tilingData.swizzlDirect = swizzlDirect;
  tilingData.swizzlCount = swizzlCount;
  return swizzlDirect;
}

}  // namespace tiling
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_310P_COMMMON_TILING_H_
