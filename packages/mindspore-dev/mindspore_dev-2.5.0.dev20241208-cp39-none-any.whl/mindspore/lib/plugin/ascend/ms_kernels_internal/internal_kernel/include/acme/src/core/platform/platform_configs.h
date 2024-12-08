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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_CONFIGS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_CONFIGS_H_

#include <string>
#include <cstdint>
#include "acme/src/core/platform/rt_funcs.h"

namespace mindspore {
namespace acme {
constexpr auto kSoc910BPrefix = "Ascend910B";
constexpr auto kSoc910CPrefix = "Ascend910_93";
constexpr auto kSoc310PPrefix = "Ascend310P";

constexpr auto kSoc910B1 = "Ascend910B1";
constexpr auto kSoc910B2 = "Ascend910B2";
constexpr auto kSoc910B2C = "Ascend910B2C";
constexpr auto kSoc910B3 = "Ascend910B3";
constexpr auto kSoc910B4 = "Ascend910B4";
constexpr auto kSoc910B4_1 = "Ascend910B4-1";

constexpr auto kSoc910C1 = "Ascend910_9391";
constexpr auto kSoc910C1_1 = "Ascend910_9392";
constexpr auto kSoc910C2 = "Ascend910_9381";
constexpr auto kSoc910C2_1 = "Ascend910_9382";
constexpr auto kSoc910C3 = "Ascend910_9372";
constexpr auto kSoc910C4 = "Ascend910_9361";

constexpr auto kSoc310P1 = "Ascend310P1";
constexpr auto kSoc310P3 = "Ascend310P3";

class HardwareConfig {
 public:
  HardwareConfig() = default;
  ~HardwareConfig() = default;
  HardwareConfig(uint32_t core_num, uint32_t l2_size, uint32_t l1_size, uint32_t l0a_size, uint32_t l0b_size,
                 uint32_t l0c_size, uint32_t ub_size)
      : core_num_(core_num),
        l2_size_(l2_size),
        l1_size_(l1_size),
        l0a_size_(l0a_size),
        l0b_size_(l0b_size),
        l0c_size_(l0c_size),
        ub_size_(ub_size) {}

  uint32_t core_num_{0};
  uint32_t l2_size_{0};
  uint32_t l1_size_{0};
  uint32_t l0a_size_{0};
  uint32_t l0b_size_{0};
  uint32_t l0c_size_{0};
  uint32_t hbm_bandwidth_{1};
  uint32_t l2_bandwidth_{5};
  uint32_t ub_size_{0};
};

class PlatformConfigs {
 public:
  PlatformConfigs();
  ~PlatformConfigs() = default;

  static const PlatformConfigs &GetInstance() {
    static PlatformConfigs kPlatformConfigs;
    return kPlatformConfigs;
  }

  inline uint32_t GetCoreNum() const { return hw_config_.core_num_; }

  inline uint32_t GetL2Size() const { return hw_config_.l2_size_; }

  inline uint32_t GetL1Size() const { return hw_config_.l1_size_; }

  inline uint32_t GetL0aSize() const { return hw_config_.l0a_size_; }

  inline uint32_t GetL0bSize() const { return hw_config_.l0b_size_; }

  inline uint32_t GetL0cSize() const { return hw_config_.l0c_size_; }

  inline uint32_t GetHbmBandwidth() const { return hw_config_.hbm_bandwidth_; }

  inline uint32_t GetL2BandwidthSize() const { return hw_config_.l2_bandwidth_; }

  inline uint32_t GetUbSize() const { return hw_config_.ub_size_; }

  const HardwareConfig &GetConfigByVersion(const std::string &soc_version) const;

 private:
  void Init();

  HardwareConfig hw_config_;
  std::string soc_version_;
};

inline bool IsSocMatch(const std::string &soc_str) {
  static const auto soc_name = RtFuncs::GetInstance().GetSocVersion();
  return soc_name.find(soc_str) != std::string::npos;
}

#define SOC_MATCH_FUNC(FUNC_NAME, SOC_STR)     \
  inline bool FUNC_NAME() {                    \
    static auto matched = IsSocMatch(SOC_STR); \
    return matched;                            \
  }

SOC_MATCH_FUNC(Is910B, kSoc910BPrefix)
SOC_MATCH_FUNC(Is910B2Serial, kSoc910B2)
SOC_MATCH_FUNC(Is910B2C, kSoc910B2C)
SOC_MATCH_FUNC(Is910B3, kSoc910B3)
SOC_MATCH_FUNC(Is910B4, kSoc910B4)
SOC_MATCH_FUNC(Is910B4_1, kSoc910B4_1)

SOC_MATCH_FUNC(Is910C, kSoc910CPrefix)
SOC_MATCH_FUNC(Is910C1, kSoc910C1)
SOC_MATCH_FUNC(Is910C2Serial, kSoc910C2)

SOC_MATCH_FUNC(Is310P, kSoc310PPrefix)
SOC_MATCH_FUNC(Is910B1, kSoc910B1)
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_CONFIGS_H_