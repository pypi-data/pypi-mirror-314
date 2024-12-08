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

#ifndef MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_H_
#define MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_H_

extern "C" void add_rms_norm_quant_do_acme(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *x1, uint8_t *x2,
                                           uint8_t *gamma, uint8_t *scales1, uint8_t *scales2, uint8_t *zero_points1,
                                           uint8_t *zero_points2, uint8_t *y1, uint8_t *y2, uint8_t *x,
                                           uint8_t *workspace, uint8_t *tiling);

#endif  // MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_H_
