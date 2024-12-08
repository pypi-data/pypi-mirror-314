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
#ifndef ADD_PARAMS_H_
#define ADD_PARAMS_H_

#include "ms_int_types.h"
#include "op_param.h"
#include <set>

namespace mindspore {
namespace internal {
const static std::set<TensorDType> ADD_SUPPORT_DTYPE{
  TensorDType::TENSOR_DTYPE_FLOAT,
  TensorDType::TENSOR_DTYPE_FLOAT16,
  TensorDType::TENSOR_DTYPE_INT32,
  TensorDType::TENSOR_DTYPE_BF16,
};
struct AddParam : public OpParam {
  TensorDType input1_dtype_;
  TensorDType input2_dtype_;
  DIMS input1_dims_;
  DIMS input2_dims_;
  bool canSupport() {
    if (ADD_SUPPORT_DTYPE.find(input1_dtype_) == ADD_SUPPORT_DTYPE.end() || input1_dims_ != input2_dims_) {
      return false;
    }
    if (input1_dims_ == input2_dims_) {
      return false;
    }
    if (std::abs(int(input1_dims_.size()) - int(input2_dims_.size())) > 1) {
      return false;
    }
    DIMS big = input1_dims_;
    DIMS small = input2_dims_;
    if (input1_dims_.size() < input2_dims_.size()) {
      big = input2_dims_;
      small = input1_dims_;
    }
    int offset = big.size() == small.size() ? 0 : 1;
    uint32_t minShapeSize = 1;
    for (size_t i = big.size() - 1; i > 0; --i) {
      minShapeSize *= big[i];
      if (big[i] != small[i - offset]) {
        return false;
      }
    }
    if (minShapeSize % 32 != 0) {
      return false;
    }
    return true;
  }
};
}  // namespace internal
}  // namespace mindspore
#endif
