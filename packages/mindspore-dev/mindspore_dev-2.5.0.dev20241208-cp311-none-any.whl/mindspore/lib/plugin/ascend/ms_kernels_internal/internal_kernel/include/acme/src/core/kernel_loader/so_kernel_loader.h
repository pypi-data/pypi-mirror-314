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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_LOADER_SO_KERNEL_LOADER_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_LOADER_SO_KERNEL_LOADER_H_

#include <unordered_map>

#define QUERY_KERNEL_FUNCTION(FUNC_VAR, FUNC_DECLARE, OP_NAME, FUNC_NAME)                          \
  static auto FUNC_VAR =                                                                           \
    reinterpret_cast<FUNC_DECLARE>(SoKernelLoader::GetInstance().QueryHandle(OP_NAME, FUNC_NAME)); \
  if (FUNC_VAR == nullptr) {                                                                       \
    MSOP_LOG(ERROR) << "Can't find kenrel function for " << OP_NAME;                               \
    return kAcmeError;                                                                             \
  }

namespace mindspore {
namespace acme {
class SoKernelLoader {
 public:
  SoKernelLoader();
  ~SoKernelLoader();

  static SoKernelLoader &GetInstance() {
    static SoKernelLoader kSoKernelLoader;
    return kSoKernelLoader;
  }

  void Init();

  void *QueryHandle(const std::string &op_name, const std::string &func_name);

 private:
  std::unordered_map<std::string, void *> dynamic_lib_handle_map_;
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_LOADER_SO_KERNEL_LOADER_H_