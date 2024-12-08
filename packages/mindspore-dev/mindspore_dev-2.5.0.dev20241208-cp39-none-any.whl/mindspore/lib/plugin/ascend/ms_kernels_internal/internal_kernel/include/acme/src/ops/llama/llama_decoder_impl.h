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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_LLAMA_DECODER_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_LLAMA_DECODER_IMPL_H_

#include <map>
#include <memory>
#include <string>
#include <vector>
#include "acme/src/ops/llama/butils.h"
#include "acme/src/ops/llama/decoder_llama.h"
#include "acme/src/ops/llama/boost_kernel.h"
#include "acme/src/ops/llama/quant.h"
#include "acme/src/ops/llama/cache_mgr.h"

namespace mindspore {
namespace acme {

struct OpLlamaDecoderParam : public mindspore::acme::BoostParam {
  TransformerParamT transformer_param_;
};

using OpLlamaDecoderParamPtr = std::shared_ptr<OpLlamaDecoderParam>;

class DecoderLlamaImpl : public BoostKernel {
 public:
  explicit DecoderLlamaImpl(const OpLlamaDecoderParamPtr &param)
      : BoostKernel(param), inputs_device_buf_(ENCODER_LAST_IDX), outputs_device_buf_(ENCODER_OUTPUT_LAST_IDX) {}
  virtual ~DecoderLlamaImpl() {
    if (prompt_mask_ != nullptr) FreeDevice(prompt_mask_);
    prompt_mask_ = nullptr;
    if (inc_mask_ != nullptr) FreeDevice(inc_mask_);
    inc_mask_ = nullptr;
    llama_decoder_delete<aclFloat16>(decoder_llama_executer_);
    decoder_llama_executer_ = nullptr;
    if (kv_cache_) FreeDevice(kv_cache_);
    kv_cache_ = nullptr;
  }
  bool Init() override;
  void SetWorkSpace(const std::vector<DeviceRawBuf> &workspace) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  uint64_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<TensorDesc> &inputs, std::vector<TensorDesc> &outputs) override;
  bool InitInputs(TransformerParamT *transformer_param);
  bool InitParam(TransformerParamT *transformer_param);
  bool CreateMask(TransformerParamT *transformer_param);
  bool InitData(TransformerParamT *transformer_param);
  std::vector<Tensor3 *> GetWeights(const std::map<std::string, Tensor *> *map);
  void SetCacheMgr(CacheMgr *cm) { cache_mgr_ = cm; }

 private:
  static void *prompt_mask_;
  static void *inc_mask_;
  void *kv_cache_ = nullptr;
  std::vector<Quant> inputs_device_buf_;
  std::vector<void *> outputs_device_buf_;
  void *workspace_addr_ = nullptr;
  void *decoder_llama_executer_ = nullptr;
  size_t ws_size_ = 0;
  DeviceRawBuf tiling_buf_;
  Tensor3 *GetWeight(const std::map<std::string, Tensor *> *map, const std::string &key);
  void SetInput(int index, int idx);
  Tensor *GetInputTensor(int idx);
  int weight_start_ = 0;
  CacheMgr *cache_mgr_;
};
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_LLAMA_DECODER_IMPL_H_
