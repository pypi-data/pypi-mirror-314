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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_OPT_ALLOCATOR_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_OPT_ALLOCATOR_H_

#include <map>

namespace mindspore {
class OptAllocator {
 public:
  explicit OptAllocator(size_t aligned_size = 32) : align_size_(aligned_size) {}
  ~OptAllocator() {}
  size_t Malloc(size_t size);
  void Free(size_t offset);
  size_t total_size() { return heap_; }

 private:
  size_t FindFree(size_t size);
  void Reorder(size_t addr);
  std::map<size_t, size_t> arena_;
  std::map<size_t, size_t> alloc_;
  size_t heap_ = 0;
  size_t align_size_;
};
};      // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_OPT_ALLOCATOR_H_
