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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_CACHE_MGR_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_CACHE_MGR_H_

#include <map>
#include <queue>
#include <memory>
#include <vector>

namespace mindspore {
namespace acme {

typedef void *ObjHandleT;

typedef struct {
  ObjHandleT oh_;
  size_t base_offset_;
  int page_num_;
  int64_t page_size_;
  int hid_;        // kv_head_num_ * head_size
  int type_size_;  // FP16, int8
  int table_id_;
} CmTblDesc;

typedef enum {
  NORMAL,
  SHARED = 1,
} PageAttrE;

typedef struct {
  int tbl_id_;
  size_t page_id_;
  PageAttrE attribute;
} PageIdDescT;

typedef struct {
  std::vector<PageIdDescT> shared_page_;
  std::vector<int> batch_ids_;
} SharedPageDescT;

// Assumption: page allocation is the same for all layers
typedef struct {
  std::vector<std::vector<PageIdDescT>> user_page_;
  std::vector<SharedPageDescT> shared_group_;
} UserPageUsageT;

class CacheMgr {
 public:
  CacheMgr(int num_layers, int page_num, int64_t page_size, int hid, int type_size)
      : num_layers_(num_layers), page_num_(page_num), page_size_(page_size), hid_(hid), type_size_(type_size) {
    for (size_t i = 0; i < max_tables_; i++) {
      q_tables_.push(i);
    }
    InitQPages(page_num);
  }
  ~CacheMgr() {
    if (block_table_h_) free(block_table_h_);
    block_table_h_ = nullptr;
  }

  int AllocTable();
  int FreeTable(int table_id);
  std::shared_ptr<CmTblDesc> getTableFromId(int tbl_id, int layer_id);
  size_t GetKVOffsetfromLayerID(int tbl_id, int layer_id);
  size_t GetKVLen(int tbl_id, int layer_id);
  int CopyActBlockTable(void *mode, void *batch_2_batch, void *block_table, void *act_block_table, int batch_size,
                        int tbl_id);
  int AssignBlockAllocation(void *bvl, void *mode, void *block_table, std::vector<std::vector<PageIdDescT>> user_page,
                            int tbl_id, int batch_size);
  int PrepareUserPage(std::vector<std::vector<PageIdDescT>> &user_page, int tbl_id, int batch_size, void *bvl,
                      void *mode);
  int InitBlockTableForGetSysWs(void *block_table, int tbl_id, int batch_size, int max_seq);
  int FreeTablePerLayer(int table_id, int layer_id);
  void SetMetaData(UserPageUsageT *user_page) { user_page_ = user_page; }
  UserPageUsageT *getMetaData() { return user_page_; }

 private:
  void InitQPages(int page_num);

 private:
  int num_layers_;
  int page_num_;
  int64_t page_size_;
  int hid_;
  int type_size_;
  int max_tables_ = 10000;
  int table_cnt_ = 0;
  std::queue<int32_t> q_free_pages_;
  std::queue<int> q_tables_;
  void *block_table_h_ = nullptr;
  UserPageUsageT *user_page_ = nullptr;
  std::map<std::pair<int, int>, std::shared_ptr<CmTblDesc>> tabels_map_;  // key = {table_id, layer_id}
};

}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_CACHE_MGR_H_
