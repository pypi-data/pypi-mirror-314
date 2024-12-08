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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_GRAPH_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_GRAPH_H_

#include <cstring>
#include <algorithm>
#include <map>
#include <numeric>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>
#include "acme/src/ops/llama/boost_kernel.h"
#include "acme/src/ops/llama/quant.h"

#pragma once
namespace mindspore {
namespace acme {

using dict = std::map<std::string, Tensor *>;
class Graph {
 public:
  explicit Graph(int device_id) : device_id_(device_id) {}
  ~Graph() { FreeMem(); }
  std::vector<Tensor *> AddLayer(BoostKernel *kernel, std::vector<Tensor *> *inputs,
                                 const std::vector<Tensor3 *> &w_inputs, std::string kernel_name);
  void AddInput(Tensor *input) { in_tensors_.push_back(input); }
  void AddOutput(Tensor *output) { out_tensors_.push_back(output); }

  size_t GetWorkspace() {
    size_t max = 0;
    for (auto &k : kernels_) {
      auto cur = k->GetWorkSpaceSize();
      if (!cur.empty()) max = std::max(max, cur.at(0));
    }
    return max;
  }

  void SetWorkspace(const std::vector<DeviceRawBuf> &workspace) {
    for (auto &k : kernels_) {
      k->SetWorkSpace(workspace);
    }
  }

  int Launch();

  int InferShape(const std::vector<TensorDesc> &input_desc, std::vector<TensorDesc> &output_desc);

  static void SetTensorDataSize(Tensor *tensor) {
    int elem_size = GetTensorElementSize(tensor->desc.dtype);
    tensor->dataSize = tensor->Numel() * elem_size;
  }

  Tensor *CreateTensor(DIMS dims, TensorFormat format, TensorDType dtype, bool free_list = true) {
    auto t = new (std::nothrow) Tensor();
    if (!t) return nullptr;
    t->desc.dims = dims;
    t->desc.format = format;
    t->desc.dtype = dtype;
    t->hostData = nullptr;
    t->data = nullptr;
    Graph::SetTensorDataSize(t);
    if (free_list) all_tensors_.push_back(t);
    return t;
  }
  static Tensor *CreateTensorStatic(DIMS dims, TensorFormat format, TensorDType dtype) {
    auto t = new Tensor();
    if (!t) return nullptr;
    t->desc.dims = dims;
    t->desc.format = format;
    t->desc.dtype = dtype;
    t->hostData = nullptr;
    t->data = nullptr;
    Graph::SetTensorDataSize(t);
    return t;
  }
  std::vector<Tensor *> &GetInputs() { return in_tensors_; }
  std::vector<Tensor *> &GetOutputs() { return out_tensors_; }
  void *get_alt_stream() { return alt_stream_; }
  void *get_stream() { return stream_; }
  bool AllocTensors();
  bool ReAllocTensors();
  size_t get_device_memory_size() { return device_memory_size_; }
  size_t get_weight_memory_size() { return w_total_; }
  int SetAffinity(int device);
  bool AclInit();

  int CkptCreate(const dict *dict, std::string name);
  static int CreateDictFromCKPT(dict *dict, std::string name);

 private:
  cpu_set_t cpuAffinity(int device);
  int CopyData(Tensor *t);
  std::vector<BoostKernel *> get_kernels() { return kernels_; }
  int SetWeights(const std::vector<Tensor3 *> &layer_weights, std::vector<Tensor *> *layer_inputs);
  void FreeMem();
  std::vector<BoostKernel *> kernels_;
  std::vector<Tensor *> in_tensors_;
  std::vector<Tensor *> out_tensors_;
  std::set<Tensor *> weight_tensor_;
  std::vector<Tensor *> all_tensors_;
  std::string model_name_;
  int layers_num_ = 0;
  void *stream_ = nullptr;
  void *alt_stream_ = nullptr;
  void *acl_ctx_ = nullptr;
  size_t device_memory_size_ = 0;
  void *device_memory_base_addr_ = nullptr;
  std::unordered_map<Tensor *, size_t> offset_map_;
  size_t w_total_ = 0;
  int device_id_;
  int pysical_dev_;
  thread_local static bool th_affinity_setup_;
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_GRAPH_H_
