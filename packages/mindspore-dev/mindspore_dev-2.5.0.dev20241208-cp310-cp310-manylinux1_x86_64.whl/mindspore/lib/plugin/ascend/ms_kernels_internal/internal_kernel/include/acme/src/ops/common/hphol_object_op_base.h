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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_CSL_OBJECT_OP_BASE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_CSL_OBJECT_OP_BASE_H_

#include "acme/src/ops/common/object_op_base.h"
#include "hphol_kernels/op_tiling/include/tiling_util.h"

namespace mindspore {
namespace acme {
inline ms_optiling::DataType ToHpholDtype(DataType dt) {
  switch (dt) {
    case kTypeFloat16:
      return ms_optiling::DTYPE_FLOAT16;
    case kTypeFloat32:
      return ms_optiling::DTYPE_FLOAT;
    case kTypeInt32:
      return ms_optiling::DTYPE_INT32;
    case kTypeInt64:
      return ms_optiling::DTYPE_INT64;
    default:
      return ms_optiling::DTYPE_UNKNOWN;
  }
}

inline ms_optiling::TensorFormat ToHpholFormat(TensorFormat format) {
  switch (format) {
    case kFormatNCHW:
      return ms_optiling::FORMAT_NCHW;
    case kFormatND:
      return ms_optiling::FORMAT_ND;
    default:
      return ms_optiling::FORMAT_UNKNOWN;
  }
}

inline ms_optiling::TensorOpDesc ToHpholTensorDesc(const ArgDesc &arg_desc) {
  return ms_optiling::TensorOpDesc(arg_desc.GetShape(), ToHpholDtype(arg_desc.GetDtype()),
                                   ToHpholFormat(arg_desc.GetFormat()));
}

class HpholObjectOpBase : public ObjectOpBase {
 public:
  HpholObjectOpBase(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                    const std::string &op_name);

  virtual ~HpholObjectOpBase() = default;

 protected:
  AcmeStatus RegisterHpholKernel(const std::string &kernel_name);

  ms_optiling::PlatformInfo platform_info_;
};

#define REG_HPHOL_KERNEL(kernel_name)                                       \
  auto status = RegisterHpholKernel(kernel_name);                           \
  if (status != kAcmeOk) {                                                  \
    MSOP_LOG(EXCEPTION) << "Failed to register kernel for " << kernel_name; \
    return kAcmeError;                                                      \
  }
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_CSL_OBJECT_OP_BASE_H_