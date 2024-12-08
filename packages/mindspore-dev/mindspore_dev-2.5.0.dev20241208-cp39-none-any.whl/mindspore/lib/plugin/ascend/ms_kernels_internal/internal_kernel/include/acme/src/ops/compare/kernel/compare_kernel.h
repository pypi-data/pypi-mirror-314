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

#ifndef MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_COMPARE_KERNEL_COMPARE_KERNEL_H_
#define MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_COMPARE_KERNEL_COMPARE_KERNEL_H_
#include <stdint.h>
#define BIT_SIZE 8
extern "C" void compare(uint32_t blockdim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                        uint8_t *tiling, uint32_t tiling_key, uint32_t broadcast_mode, uint32_t compare_mode);
#endif  // MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_COMPARE_KERNEL_COMPARE_KERNEL_H_