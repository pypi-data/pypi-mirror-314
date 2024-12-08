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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_RMS_NORM_RMSNORM_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_RMS_NORM_RMSNORM_TILING_H_

#include <sstream>

#include "rms_norm_tiling_data.h"
#include "acme/include/base_type.h"

namespace mindspore {
namespace acme {
AcmeStatus RmsNormTilingImpl(RawHostAddr &host_ptr, const InputsDescList &inputs, const float eps,
                             uint32_t *block_dims);
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_RMS_NORM_RMSNORM_TILING_H_