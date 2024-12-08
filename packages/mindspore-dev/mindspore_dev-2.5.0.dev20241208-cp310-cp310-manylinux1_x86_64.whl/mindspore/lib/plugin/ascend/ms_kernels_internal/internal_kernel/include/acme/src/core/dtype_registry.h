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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_KERNEL_REGISTRY_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_KERNEL_REGISTRY_H_

#include <map>

#include "acme/include/base_type.h"
#include "acme/src/core/kernel_loader/hphol_kernel_loader.h"

namespace mindspore {
namespace acme {
enum BackendType : size_t {
  kBEAsd = 0,
  kBEAcme = 1,
  kBEMax = 2,
};

static const std::vector<std::string> kBackendName = {"Asd", "Acme"};

class DtypeRegistry {
 public:
  DtypeRegistry();
  virtual ~DtypeRegistry() = default;

  static DtypeRegistry *GetInstance();
  void RegisterOpName2NzOpName(const std::string &op_name, const std::string &nz_op_name);
  std::string ConvertOpName2NzOpName(const std::string &op_name) const;
  void RegisterAcmeDtypes(const std::string &op_name, const InOutDtypesList &dtype_list,
                          const InOutIndicesType &optional_arg_indices);
  void RegisterAcmeDtypes(const std::string &op_name, const InOutDtypesList &dtype_list);
  void RegisterAcmeDtypes(const std::string &op_name, const InOutDtypesTargetMap &dtype_map);

  void RegisterAsdDtypes(const std::string &op_name, const InOutDtypesList &dtype_list,
                         const InOutIndicesType &optional_arg_indices);
  void RegisterAsdDtypes(const std::string &op_name, const InOutDtypesList &dtype_list);
  void RegisterAsdDtypes(const std::string &op_name, const InOutDtypesTargetMap &dtype_map);

  void PrintSupportDtypes(const std::string &op_name);
  bool IsDtypesSupported(const std::string &op_name, const InputDataTypes &in_dtypes, const InputDataTypes &out_dtypes);
  bool IsSupported(const std::string &op_name, const InputDataTypes &in_dtypes, const InputDataTypes &out_dtypes,
                   const InOutDtypesList &dtypes_support_list, BackendType backend);

 private:
  void RegisterDtypes(const std::string &op_name, const InOutDtypesList &dtype_list, BackendType backend);
  void RegisterDtypes(const std::string &op_name, const InOutDtypesTargetMap &dtype_map, BackendType backend);
  void RegisterDtypes(const std::string &op_name, const InOutDtypesList &dtype_list,
                      const InOutIndicesType &optional_arg_indices, BackendType backend);

  std::vector<std::map<std::string, InOutDtypesList>> dtype_support_map_;
  std::vector<std::map<std::string, InOutIndicesType>> optional_arg_indices_;
  std::map<std::string, std::string> op_name_2_nz_op_name_map_;
};

class OpNameRegistrar {
 public:
  explicit OpNameRegistrar(const std::string &op_name, const std::string &nz_op_name) {
    DtypeRegistry::GetInstance()->RegisterOpName2NzOpName(op_name, nz_op_name);
  }
  ~OpNameRegistrar() = default;
};
#define ACME_KERNEL_REG_OP_NAME(NAME, NZ_NAME) static const OpNameRegistrar g_##NAME##_acme_name_reg(NAME, NZ_NAME)

class DtypeRegistrar {
 public:
  explicit DtypeRegistrar(const std::string &op_name, const InOutDtypesList &dtype_list,
                          const InOutIndicesType &optional_arg_indices) {
    DtypeRegistry::GetInstance()->RegisterAcmeDtypes(op_name, dtype_list, optional_arg_indices);
  }

  explicit DtypeRegistrar(const std::string &op_name, const InOutDtypesList &dtype_list) {
    DtypeRegistry::GetInstance()->RegisterAcmeDtypes(op_name, dtype_list);
  }

  explicit DtypeRegistrar(const std::string &op_name, const InOutDtypesTargetMap &dtype_map) {
    DtypeRegistry::GetInstance()->RegisterAcmeDtypes(op_name, dtype_map);
  }
  ~DtypeRegistrar() = default;
};

class ObjectKDtypeRegisterHelper {
 public:
  explicit ObjectKDtypeRegisterHelper(const std::string &op_name, const std::string &kernel_name) {
    auto dtypes = HpholKernelLoader::GetInstance().GetInOutDtypesByKernelName(kernel_name);
    if (!dtypes.empty()) {
      auto optional_indices = std::move(HpholKernelLoader::GetInstance().GetInOutOptionalIndices(kernel_name));
      DtypeRegistry::GetInstance()->RegisterAcmeDtypes(op_name, dtypes, optional_indices);
    }
  }
  ~ObjectKDtypeRegisterHelper() = default;
};

#define ACME_KERNEL_REG_BY_DTYPES(NAME, DTYPES) static const DtypeRegistrar g_##NAME##_acme_reg(NAME, DTYPES)
#define ACME_KERNEL_REG_BY_DTYPES_WITH_OPTIONAL(NAME, DTYPES, OPTIONAL) \
  static const DtypeRegistrar g_##NAME##_acme_reg(NAME, DTYPES, OPTIONAL)
#define ACME_KERNEL_REG_BY_TARGET_DTYPES(NAME, TARGET_DTYPES) \
  static const DtypeRegistrar g_##NAME##_target_acme_reg(NAME, TARGET_DTYPES)

#define ACME_OBJECT_KERNEL_REG(NAME, KERNEL_NAME) \
  static const ObjectKDtypeRegisterHelper g_##NAME##_acme_object_kernel_reg(NAME, KERNEL_NAME)

class AsdOpDtypeRegistrar {
 public:
  explicit AsdOpDtypeRegistrar(const std::string &op_name, const InOutDtypesList &dtype_list) {
    DtypeRegistry::GetInstance()->RegisterAsdDtypes(op_name, dtype_list);
  }

  explicit AsdOpDtypeRegistrar(const std::string &op_name, const InOutDtypesTargetMap &dtype_map) {
    DtypeRegistry::GetInstance()->RegisterAsdDtypes(op_name, dtype_map);
  }
  ~AsdOpDtypeRegistrar() = default;
};

#define ASDOP_KERNEL_REG_BY_DTYPES(NAME, DTYPES) static const AsdOpDtypeRegistrar g_##NAME##_asd_reg(NAME, DTYPES)
#define ASDOP_KERNEL_REG_BY_TARGET_DTYPES(NAME, TARGET_DTYPES) \
  static const AsdOpDtypeRegistrar g_##NAME##_target_asd_reg(NAME, TARGET_DTYPES)
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_KERNEL_REGISTRY_H_