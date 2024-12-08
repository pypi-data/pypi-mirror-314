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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_COMM_ADAPTER_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_COMM_ADAPTER_H_
#include <memory>
#include <vector>
#include "hccl/hccl.h"
#include <hccl/hccl_types.h>
#ifdef USE_LCCL
#include "Lccl/include/lccl.h"
using LcalCommPtr = std::shared_ptr<Lcal::LcalComm>;
#endif

namespace mindspore {
class CommAdapter {
 public:
  const int root_rank = 0;
  const uint32_t HCCL_ROOT_INFO_BYTES = 4108;  // 4108: root info length
  CommAdapter();
  explicit CommAdapter(const CommAdapter &hccl) = delete;
  virtual ~CommAdapter();
  static CommAdapter &GetInstance();
  HcclResult Init(void *com);
  int get_device() { return mpi_mode_ ? rank_id_ : dev_id_; }
  int get_rank() { return rank_id_; }
  int get_pysical_device() { return dev_id_; }
  int get_size() { return rank_size_; }
  HcclResult AllGather(void *send_buff, void *recv_buff, uint64_t count, HcclDataType dataType, void *stream);
  HcclResult AllSumReduce(void *send_buff, void *recv_buff, uint64_t count, void *stream);
#ifndef USE_LCCL
  HcclResult Gather(void *send_buff, void *recv_buff, uint64_t count, int dest, void *stream);
#else
  LcalCommPtr &get_lcal() { return lcal_comm_; }
#endif
  HcclResult HcclSync(void *stream);
  void test_reduce(void *stream);

 private:
#ifdef USE_LCCL
  HcclResult LcclInit();
  LcalCommPtr lcal_comm_;
  Lcal::Lccl *lccl_comm_;
#endif
  HcclResult HcclInit(void *com);
  HcclResult get_mpi_proc();
  HcclResult set_device_sat_mode();
  std::vector<int> getAviDevs(const char *devs);
  int dev_id_ = -1;
  int rank_id_ = 0;
  int rank_size_ = 1;
  HcclComm hccl_comm_ = nullptr;
  HcclRootInfo comm_id_;
  bool initialized_ = false;
  bool mpi_mode_ = false;
};

};      // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_COMM_ADAPTER_H_
