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
#ifndef SUB_PARAMS_H_
#define SUB_PARAMS_H_

#include "ms_int_types.h"
#include "op_param.h"
#include <set>

namespace mindspore {
namespace internal {
struct SubParam : public OpParam {
  TensorDType input1_dtype_;
  TensorDType input2_dtype_;
  DIMS input1_dims_;
  DIMS input2_dims_;
};
}  // namespace internal
}  // namespace mindspore
#endif
