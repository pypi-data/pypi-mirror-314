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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_REGISTER_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_REGISTER_H_

#include <vector>
#include <memory>

namespace mindspore {
namespace acme {
extern const char *kMatmulKernelName;
extern const char *kMultiWeightMatmulKernelName;

extern const char *kMatmulAddRmsNormKernel_Fp16_Fp16;
extern const char *kMatmulAddRmsNormKernel_Fp16_Fp32;
extern const char *kMatmulAddRmsNormKernel_Fp16_BF16;
extern const char *kMatmulAddRmsNormKernel_BF16_Fp16;
extern const char *kMatmulAddRmsNormKernel_BF16_Fp32;
extern const char *kMatmulAddRmsNormKernel_BF16_BF16;

extern const char *kFlashAttentionScore_Fp16_BNSD_Tri;
extern const char *kFlashAttentionScore_Fp16_BSH_Tri;
extern const char *kFlashAttentionScore_BF16_BNSD_Tri;
extern const char *kFlashAttentionScore_BF16_BSH_Tri;
extern const char *kFlashAttentionScore_FP16_BNSD_Full;
extern const char *kFlashAttentionScore_Fp16_BSH_Full;
extern const char *kFlashAttentionScore_BF16_BNSD_Full;
extern const char *kFlashAttentionScore_BF16_BSH_Full;

extern const char *kPagedAttention;
extern const char *kPagedAttentionV2;

extern const char *kPpMatmulInt8NZ;
extern const char *kPpMatmulInt8NZCompress;

using BinBufPtr = std::shared_ptr<std::vector<char>>;

class KernelRegister {
 public:
  KernelRegister();
  ~KernelRegister() = default;

  static const KernelRegister &GetInstance() {
    static const KernelRegister kKernelRegister;
    return kKernelRegister;
  }

  void Register();

 private:
  std::vector<BinBufPtr> bin_buf_ptrs_;
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_REGISTER_H_