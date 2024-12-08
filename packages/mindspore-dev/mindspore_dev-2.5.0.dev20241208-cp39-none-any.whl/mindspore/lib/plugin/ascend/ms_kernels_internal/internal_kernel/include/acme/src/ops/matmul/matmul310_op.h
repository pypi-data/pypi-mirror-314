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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_MATMUL310_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_MATMUL310_OP_H_

#include "acme/include/acme_op.h"
namespace mindspore {
namespace acme {
class MatmulOp310 : public AcmeOp {
 public:
  MatmulOp310(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
              const MatmulParam &param, const std::string &op_name);
  ~MatmulOp310() = default;
  OpType GetOpType() override { return kOpTypeAICore; }

  std::vector<size_t> GetWorkspaceSize() const override;

  AcmeStatus Launch(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                    void *stream, const std::string &op_fullname = "");
  std::string DumpTiling(const RawHostAddr host_ptr) const override;
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  AcmeStatus InitImpl() override;
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  virtual AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                                const WsAddrList &ws_ptrs, void *stream) override;

 private:
  uint32_t m_;
  uint32_t n_;
  uint32_t k_;
  std::shared_ptr<void> tilingData_;
  std::string soc_name_{"UnknownSoc"};
  MatmulParam param_;
  int usedCoreNum_;
};
}  // namespace acme
}  // namespace mindspore
#endif  //  MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_MATMUL310_OP_H_
