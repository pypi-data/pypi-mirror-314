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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_GEMM_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_GEMM_H_

#include <string>
#include <vector>
#include <functional>
#include "acl/acl.h"
#include "aclnn/acl_meta.h"
#include "acme/src/ops/llama/quant.h"
namespace std {
template <>
class hash<std::vector<uint64_t>> {
 public:
  std::hash<std::string> st_fn;
  uint64_t cc = st_fn("gemm");
  uint64_t operator()(const std::vector<uint64_t> &in) const {
    const std::vector<uint64_t> prime = {280859, 317587, 318281, 335833, 364393, 589583,
                                         610661, 646271, 646879, 664967, 679907};
    uint64_t sum = cc;
    for (size_t i = 0; i < in.size(); i++) {
      sum += in[i] * prime[i % prime.size()] + (sum >> 32);
    }
    return sum;
  }
};
};  // namespace std

namespace mindspore::acme {
class Gemm {
 public:
  virtual ~Gemm() { clean(); }
  using aclnn_fn = std::function<aclnnStatus(void *, uint64_t, aclOpExecutor *, void *)>;
  Gemm() = default;
  aclnnStatus init(int B, int M, int N, int K, void *a, Quant *b, void *c, void *stream, bool a_nz = false,
                   bool b_nz = false, bool c_nz = false, bool ta = false, bool tb = false, void *bias = nullptr,
                   int lda = -1, int ldb = -1, int ldc = -1);
  aclnnStatus compute(void *workspace, uint64_t workspace_size, void *stream);
  aclnnStatus execute(int B, int M, int N, int K, void *a, Quant *b, void *c, void *workspacePtr,
                      uint64_t workspace_size, void *stream, bool a_nz = false, bool b_nz = false, bool c_nz = false,
                      void *bias = nullptr, int lda = -1, int ldb = -1, int ldc = -1, bool ta = false, bool tb = false);

  uint64_t GetSysWs(int B, int M, int N, int K, void *stream, bool a_nz = false, bool b_nz = false, bool c_nz = false,
                    int lda = -1, int ldb = -1, int ldc = -1);
  static std::vector<int64_t> calcStride(const std::vector<int64_t> &shape);

 private:
  aclnnStatus initQuant(int M, int N, int K, void *a, Quant *b, void *c, void *bias, bool a_nz, bool b_nz, bool c_nz);
  aclnnStatus initAclNN(int B, int M, int N, int K, void *a, Quant *b, void *c, bool a_nz = false, bool b_nz = false,
                        bool c_nz = false, void *bias = nullptr, int lda = -1, int ldb = -1, int ldc = -1);
  aclnnStatus initAclGemm(int M, int N, int K, void *a, Quant *b, void *c, bool ta, bool tb, int lda, int ldb, int ldc);
  void clean();
  bool HitCache(const std::vector<std::string> &list, int B, int M, int N, int K, void *a, Quant *b, void *c,
                void *bias, bool ta = false, bool tb = false);
  void initMsMatmul();

  uint64_t workspace_size_ = 0;
  aclOpExecutor *executor_ = nullptr;
  std::vector<aclTensor *> vcollect_;
  std::vector<aclScalar *> scollect_;
  aclnn_fn compute_ = nullptr;
  bool is_bias_ = false;
  bool is_bmm_ = false;
  bool is_blas_ = false;
  bool is_quant_ = false;
  bool transpose_a_ = false;
  bool transpose_b_ = false;
  void *matrix_a_ = nullptr;
  void *matrix_b_ = nullptr;
  void *matrix_c_ = nullptr;
  int m_;
  int n_;
  int k_;
  void *alpha_;
  void *beta_;
  int rank_{0};
};

#ifdef MATMUL_REDUCE
class GemmDistribute {
 public:
  aclnnStatus execute(int M, int N, int K, void *a, bool transpose_a, void *b, bool transpose_b, void *c, void *bias,
                      void *workspace, uint64_t workspace_size, void *stream);
  uint64_t GetSysWs(int M, int N, int K, bool transpose_a, bool transpose_b);

 private:
  std::shared_ptr<Lcal::Lcoc> init(int M, int N, int K, bool transpose_a, bool transpose_b);
  std::shared_ptr<Lcal::Lcoc> lcoc_ptr_;
};

#endif

};      // namespace mindspore::acme
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_GEMM_H_
