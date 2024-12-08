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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_KERNEL_MATMUL_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_KERNEL_MATMUL_KERNEL_H_
extern "C" void MatMulOp(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *gm_a, uint8_t *gm_b, uint8_t *gm_bias,
              uint8_t *gm_scale, uint8_t *gm_c, uint8_t *tilingData);
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_MATMUL_KERNEL_MATMUL_KERNEL_H_