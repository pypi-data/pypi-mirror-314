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
#ifndef ELEWISE_PARAMS_H_
#define ELEWISE_PARAMS_H_

#include "ms_int_types.h"
#include "op_param.h"
#include <set>
namespace mindspore {
namespace internal {
#define MAX_ELEWISE_SHAPE_LEN 16
struct ElewiseBaseParam : public OpParam {
  size_t dims_;
  int32_t dtype_;
};

struct ElewiseUnaryParam : public ElewiseBaseParam {};

struct ElewiseBinaryParam : public ElewiseBaseParam {
  DIMS input0_dims_;
  DIMS input1_dims_;
  uint32_t broadcast_mode_;
  int64_t in0_shape_[MAX_ELEWISE_SHAPE_LEN];
  int64_t in1_shape_[MAX_ELEWISE_SHAPE_LEN];
};
}  // namespace internal
}  // namespace mindspore
#endif  // ELEWISE_PARAMS_H_
