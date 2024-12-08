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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_FFN_LLAMA_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_FFN_LLAMA_H_
#include <vector>
#include "acl/acl.h"
#include "aclnnop/aclnn_mm.h"
#include "aclnnop/aclnn_trans_matmul_weight.h"
#include "acme/src/ops/llama/butils.h"
#include "acme/src/ops/llama/gemm.h"
#include "acme/src/ops/llama/comm_adapter.h"
#include "acme/src/ops/llama/kernel/tiling_data.h"
#include "acme/src/ops/llama/kernel/encoder_vector_kernels.h"

namespace mindspore::acme {
template <typename T>
class FfnLlama {
 public:
  FfnLlama() = default;
  ~FfnLlama() {}

  void Prepare(Quant map_weights, Quant proj_weights, TransformerParamT *p, int vcores, int ccores) {
    vcores_ = vcores;
    map_weights_ = map_weights;
    proj_weights_ = proj_weights;
  }

  size_t GetWsSize(TransformerParamT *p) {
    size_t len = static_cast<size_t>(p->desc.batch_size_) * static_cast<size_t>(p->desc.seq_) *
                 static_cast<size_t>(p->desc.ffn_hid_dim_) * sizeof(T);
    len = ALIGN(len, ASCEND_BUF_ALIGN);
    return 3 * len;
  }

  size_t GetSysWsSize(TransformerParamT *p, void *stream) {
    return std::max(gemm0_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, 2 * p->desc.ffn_hid_dim_, p->desc.hid_dim_,
                                    stream, false, p->w_nz, false),
                    gemm1_.GetSysWs(1, p->desc.batch_size_ * p->desc.seq_, p->desc.hid_dim_, p->desc.ffn_hid_dim_,
                                    stream, false, p->w_nz, false));
  }
  int Compute(void *input, void *output, TransformerParamT *p, void *ws, void *sys_ws, size_t sys_ws_size,
              void *stream) {
    // setup expert
    size_t offset = (size_t)p->token_num_ * (size_t)p->desc.ffn_hid_dim_ * (size_t)sizeof(T);
    offset = ALIGN(offset, ASCEND_BUF_ALIGN);
    void *out_silu_and_mul = reinterpret_cast<uint8_t *>(ws) + 2 * offset;

    gemm0_.execute(1, p->token_num_, 2 * p->desc.ffn_hid_dim_, p->desc.hid_dim_, input, &map_weights_, ws, sys_ws,
                   sys_ws_size, stream, false, p->w_nz, false);
    using SiluMulFuncProto = void (*)(void *, void *, uint32_t, uint32_t, int, void *);
    QUERY_KERNEL_FUNCTION(silu_mul_kernel, SiluMulFuncProto, "llama", "KernelSiluAndMulAscendc");
    silu_mul_kernel(ws, out_silu_and_mul, p->token_num_, p->desc.ffn_hid_dim_, vcores_, stream);
    gemm1_.execute(1, p->token_num_, p->desc.hid_dim_, p->desc.ffn_hid_dim_, out_silu_and_mul, &proj_weights_, output,
                   sys_ws, sys_ws_size, stream, false, p->w_nz, false);

    if (p->rank_num_ > 1) {
      auto &ccl = CommAdapter::GetInstance();
      uint64_t count = p->token_num_ * p->desc.hid_dim_;
      ccl.AllSumReduce(output, output, count, stream);
    }
    return ACL_SUCCESS;
  }

 private:
  int vcores_;
  std::vector<aclTensor *> vcollect_;
  Gemm gemm0_;
  Gemm gemm1_;
  Quant map_weights_;
  Quant proj_weights_;
};
}  // namespace mindspore::acme
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_FFN_LLAMA_H_
