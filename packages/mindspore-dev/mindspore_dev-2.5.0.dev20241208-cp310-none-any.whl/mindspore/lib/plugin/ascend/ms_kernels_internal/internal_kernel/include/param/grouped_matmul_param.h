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
#ifndef GROUPED_MATMUL_PARAMS_H
#define GROUPED_MATMUL_PARAMS_H

#include "ms_int_types.h"
#include "op_param.h"

namespace mindspore {
namespace internal {
struct GroupedMatmulParam : public OpParam {
  /*
  split_item   inputs       weight       bias         outputs
        0:     separated    separated    separated    separated
        1:     integrated   e, k, n      e, n         separated
        2:     separated    separated    separated    integrated
        3:     integrated   e, k, n      e, n         integrated
  */
  int split_item = 0;
  int dtype = 0;  // TODO dtype 什么用处
  bool transpose_weight = false;
  int group_num = 1;
  bool has_bias = false;
};
}  // namespace internal
}  // namespace mindspore
#endif