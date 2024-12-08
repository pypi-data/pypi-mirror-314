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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_DYNAMIC_QUANT_ADD_RMS_NORM_DYNAMIC_QUANT_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_DYNAMIC_QUANT_ADD_RMS_NORM_DYNAMIC_QUANT_H_

#include "acme/src/ops/common/hphol_object_op_base.h"

namespace mindspore {
namespace acme {
class AddRmsNormDynamicQuantOp : public HpholObjectOpBase {
 public:
  AddRmsNormDynamicQuantOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                           const NormParam &param, const std::string &op_name);

  virtual ~AddRmsNormDynamicQuantOp() = default;

  std::string DumpTiling(const RawHostAddr host_ptr) const override;
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;
  OpType GetOpType() override { return kOpTypeAICore; }

 protected:
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus InitImpl() override;

 private:
  NormParam param_;
};

using AddRmsNormDynamicQuantOpPtr = std::shared_ptr<AddRmsNormDynamicQuantOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_DYNAMIC_QUANT_ADD_RMS_NORM_DYNAMIC_QUANT_H_
