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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_OBJECT_OP_BASE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_OBJECT_OP_BASE_H_

#include <set>
#include "acme/include/acme_op.h"
#include "acme/src/core/platform/rt_funcs.h"

namespace mindspore {
namespace acme {
class HostRunInfoObjectOp : public HostRunInfo {
 public:
  explicit HostRunInfoObjectOp(uint32_t block_dim, uint64_t tiling_key);
  ~HostRunInfoObjectOp() = default;

  uint32_t GetBlockDim() const override;
  uint64_t GetTilingKey() const;

  uint32_t block_dim_{0};
  uint64_t tiling_key_{0};
  uint64_t any_value0_{0};
  uint64_t any_value1_{0};
  uint64_t any_value2_{0};
  uint64_t any_value3_{0};
  uint64_t any_value4_{0};
  uint64_t any_value5_{0};
};
using HostRunInfoBinOpPtr = std::shared_ptr<HostRunInfoObjectOp>;

class ObjectOpBase : public AcmeOp {
 public:
  ObjectOpBase(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
               const std::string &op_name);

  virtual ~ObjectOpBase() = default;

  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;
  void SetTilingInfo(const TilingInfoPtr &tiling_info) override;

  uint32_t GetLaunchCoreNum() const override;

 protected:
  AcmeStatus RegisterKernel(const std::string &bin_path);
  void SetHostRunInfoObjectOp(const HostRunInfoObjectOp &run_info, HostRunInfoPtr *run_info_ptr);

  void *handle_{nullptr};
  std::vector<char> buf_;
  RtArgsEx_T args_ex_;
  std::vector<void *> args_;
  HostRunInfoBinOpPtr host_run_info_bin_op_ptr_{nullptr};
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_COMMON_OBJECT_OP_BASE_H_