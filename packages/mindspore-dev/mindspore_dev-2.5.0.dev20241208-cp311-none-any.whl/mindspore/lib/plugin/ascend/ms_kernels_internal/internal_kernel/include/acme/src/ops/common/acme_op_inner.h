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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_ACME_OP_INNER_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_ACME_OP_INNER_H_

#include "acme/include/acme_op.h"

namespace mindspore {
namespace acme {
template <typename T>
void SetHostRunInfo(const T &run_info, std::shared_ptr<T> *ori_run_info_ptr_ptr, HostRunInfoPtr *out_run_info_ptr) {
  if (out_run_info_ptr) {
    *out_run_info_ptr = std::make_shared<T>(run_info);
  }

  auto &ori_run_info_ptr = *ori_run_info_ptr_ptr;
  if (ori_run_info_ptr == nullptr) {
    ori_run_info_ptr = std::make_shared<T>(run_info);
  } else {
    *ori_run_info_ptr = run_info;
  }
}

template <typename T>
void UpdateTilingInfo(const TilingInfoPtr &tiling_info, std::shared_ptr<T> *ori_run_info_ptr_ptr,
                      RawDeviceAddr *tiling_device_addr) {
  if (tiling_info) {
    *tiling_device_addr = tiling_info->tiling_addr_;

    auto &ori_run_info_ptr = *ori_run_info_ptr_ptr;
    if (tiling_info->host_run_info_ != nullptr) {
      auto run_info_ptr = std::static_pointer_cast<T>(tiling_info->host_run_info_);
      if (ori_run_info_ptr == nullptr) {
        ori_run_info_ptr = std::make_shared<T>(*run_info_ptr.get());
      } else {
        *ori_run_info_ptr = *run_info_ptr.get();
      }
    }
  }
}
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_ACME_OP_INNER_H_