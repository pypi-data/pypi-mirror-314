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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_ARG_MAX_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_ARG_MAX_H_

#include <vector>
#include <string>
#include "acl/acl.h"
#include "aclnnop/aclnn_argmax.h"

namespace mindspore::acme {
class ArgMax {
 public:
  virtual ~ArgMax() { /* clean();*/
  }
  ArgMax() = default;
  aclnnStatus init(int batch_size, int vocab_size, int max_size, void *self, void *out, int dim = 0,
                   bool keep_dim = false);
  aclnnStatus compute(void *workspace, uint64_t workspace_size, void *stream);
  aclnnStatus execute(int batch_size, int vocab_size, int max_size, void *self, void *out, void *workspacePtr,
                      uint64_t workspace_size, void *stream, int dim = 0, bool keep_dim = false);
  uint64_t GetSysWs(int batch_size, int vocab_size, int max_size, void *stream, int dim = 0, bool keep_dim = false);

 private:
  std::vector<int64_t> calcStride(const std::vector<int64_t> &shape);
  void clean();

  uint64_t workspace_size_ = 0;
  aclOpExecutor *executor_ = nullptr;
  std::vector<aclTensor *> vcollect_;
  std::vector<aclScalar *> scollect_;
  bool keep_dims_ = false;
  void *self = nullptr;
  void *out = nullptr;
  int batch_size_;
  int vocab_size_;
  int max_size_;
};
};      // namespace mindspore::acme
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_ARG_MAX_H_
