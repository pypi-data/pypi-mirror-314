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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_LLAMA_VSL_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_LLAMA_VSL_IMPL_H_

#include <memory>
#include <vector>
#include <queue>
#include "acme/src/ops/llama/boost_kernel.h"
#include "acme/src/ops/llama/cache_mgr.h"

namespace mindspore {
namespace acme {

struct OpVslParam : public BoostParam {
  int max_seq_;
  bool paged_attention_;
  int table_id_;
  int page_num_;
  void *block_table_;
};

using OpVslParamPtr = std::shared_ptr<OpVslParam>;

class LlamaVslImpl : public BoostKernel {
 public:
  explicit LlamaVslImpl(const OpVslParamPtr &param) : BoostKernel(param) {}
  virtual ~LlamaVslImpl() {}
  bool Init() override;
  void SetWorkSpace(const std::vector<DeviceRawBuf> &workspace) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  uint64_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<TensorDesc> &inputs, std::vector<TensorDesc> &outputs) override;
  void SetCacheMgr(CacheMgr *cm) { cache_mgr_ = cm; };

 private:
  bool InitHostData();
  bool FreeHostData();
  std::vector<std::vector<mindspore::acme::PageIdDescT>> user_page_;
  int batch_size_ = 0;
  ;
  void *workspace_addr = nullptr;
  DeviceRawBuf tiling_buf_;
  std::queue<int32_t> q_;
  CacheMgr *cache_mgr_;
};
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_LLAMA_VSL_IMPL_H_
