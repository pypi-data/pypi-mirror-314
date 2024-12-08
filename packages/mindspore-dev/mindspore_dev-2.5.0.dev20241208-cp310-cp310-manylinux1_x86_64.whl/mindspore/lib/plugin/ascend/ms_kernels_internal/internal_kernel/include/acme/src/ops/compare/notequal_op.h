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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_NOTEQUAL_NOTEQUAL_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_NOTEQUAL_NOTEQUAL_OP_H_

#include "acme/src/ops/compare/compare_op.h"

namespace mindspore {
namespace acme {
class NotEqualOp : public CompareOp {
 public:
  NotEqualOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
             const std::string &op_name)
      : CompareOp(inputs_ii, outputs_ii, op_name) {}
  ~NotEqualOp() = default;
};

using NotEqualOpPtr = std::shared_ptr<NotEqualOp>;
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_NOTEQUAL_NOTEQUAL_OP_H_