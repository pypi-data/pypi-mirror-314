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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_QUANT_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_QUANT_H_
#include <vector>
#include "acme/src/ops/llama/butils.h"

namespace mindspore {
namespace acme {

class Tensor3 {
 public:
  Tensor3() = default;
  explicit Tensor3(Tensor *t) : tensor_(t) {}
  Tensor *tensor_;
  Tensor *scale_ = nullptr;
  Tensor *offset_ = nullptr;
  void Free() {
    if ((tensor_ != nullptr) && (tensor_->data != nullptr)) {
      FreeDevice(tensor_->data);
      tensor_->data = nullptr;
    };
    if ((scale_ != nullptr) && (scale_->data != nullptr)) {
      FreeDevice(scale_->data);
      scale_->data = nullptr;
    }
    if ((offset_ != nullptr) && (offset_->data != nullptr)) {
      FreeDevice(offset_->data);
      offset_->data = nullptr;
    }
  }
};

class Quant {
 public:
  enum State { idle, quant, scale, offset };
  Quant() = default;
  Quant(void *data, void *scale = nullptr, void *offset = nullptr) : data_(data), scale_(scale), offset_(offset) {}
  Quant(const Quant &q) {
    if (this != &q) {
      copy_fields(q);
    }
  }
  operator bool() { return scale_ != nullptr; }

  explicit Quant(Quant &&w) {
    if (this != &w) {
      data_ = w.data_;
      scale_ = w.scale_;
      offset_ = w.offset_;
      w.data_ = nullptr;
      w.scale_ = nullptr;
      w.offset_ = nullptr;
    }
  }
  Quant &operator=(Quant &r) {
    if (this != &r) {
      data_ = r.data_;
      scale_ = r.scale_;
      offset_ = r.offset_;
    }
    return *this;
  }

  void set_scale(void *w) { scale_ = w; }
  void set_offset(void *w) { offset_ = w; }
  void *data_ = nullptr;
  void *scale_ = nullptr;
  void *offset_ = nullptr;

 private:
  void copy_fields(const Quant &r) {
    data_ = r.data_;
    scale_ = r.scale_;
    offset_ = r.offset_;
  }
};

}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_QUANT_H_
