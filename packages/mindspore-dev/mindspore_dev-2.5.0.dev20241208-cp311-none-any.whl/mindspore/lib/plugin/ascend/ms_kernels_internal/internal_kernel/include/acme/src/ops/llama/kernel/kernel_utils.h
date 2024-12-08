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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_KERNEL_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_KERNEL_UTILS_H_

#define PIPE_CAST (2)
#define BLOCK_CAST (4 * 1024)
#define ASCEND_BUF_ALIGN (1024)
#define UP_DIV(x, y) (((x) + (y) - (1)) / (y))
#define ALIGN32(size) ((((size) + 32 - 1) / 32) * 32)
#define ALIGN(size, len) ((((size) + (len)-1) / (len)) * (len))
#define ALIGN_BY_TYPE(size, size_of_type, bytes) \
  ((((size) + ((bytes) / (size_of_type)) - 1) / ((bytes) / (size_of_type))) * ((bytes) / (size_of_type)))

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_KERNEL_UTILS_H_
