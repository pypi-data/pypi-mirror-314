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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_LOADER_OBJECT_KERNEL_LOADER_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_LOADER_OBJECT_KERNEL_LOADER_H_

#include <unordered_map>
#include <unordered_set>
#include "acme/include/base_type.h"
#include "utils/log/log.h"

namespace mindspore {
namespace acme {
constexpr auto kCoreTypeStrAIV = "AIV";
constexpr auto kCoreTypeStrAIC = "AIC";
constexpr auto kParamTypeStrRequired = "required";
constexpr auto kParamTypeStrOptional = "optional";
constexpr auto kParamTypeStrDynamic = "dynamic";

constexpr auto kDtypeStrFloat32 = "float32";
constexpr auto kDtypeStrFloat16 = "float16";
constexpr auto kDtypeStrInt8 = "int8";
constexpr auto kDtypeStrInt16 = "int16";
constexpr auto kDtypeStrUint16 = "uint16";
constexpr auto kDtypeStrUint8 = "uint8";
constexpr auto kDtypeStrInt32 = "int32";
constexpr auto kDtypeStrInt64 = "int64";
constexpr auto kDtypeStrUint32 = "uint32";
constexpr auto kDtypeStrUint64 = "uint64";
constexpr auto kDtypeStrBool = "bool";
constexpr auto kDtypeStrDouble = "double";
constexpr auto kDtypeStrComplex64 = "complex64";
constexpr auto kDtypeStrComplex128 = "complex128";
constexpr auto kDtypeStrQint8 = "qint8";
constexpr auto kDtypeStrQint16 = "qint16";
constexpr auto kDtypeStrQint32 = "qint32";
constexpr auto kDtypeStrQuint8 = "quint8";
constexpr auto kDtypeStrQuint16 = "quint16";
constexpr auto kDtypeStrBf16 = "bf16";
constexpr auto kDtypeStrBfloat16 = "bfloat16";
constexpr auto kDtypeStrInt4 = "int4";
constexpr auto kDtypeStrUint1 = "uint1";
constexpr auto kDtypeStrInt2 = "int2";

constexpr auto kFormatStrNCHW = "NCHW";
constexpr auto kFormatStrNHWC = "NHWC";
constexpr auto kFormatStrND = "ND";
constexpr auto kFormatStrNC1HWC0 = "NC1HWC0";
constexpr auto kFormatStrFRACTAL_Z = "FRACTAL_Z";

constexpr auto kMagicStrELF_AIVEC = "RT_DEV_BINARY_MAGIC_ELF_AIVEC";

enum CoreType : int8_t {
  kCoreTypeUnknown = 0,
  kCoreTypeAIV,
  kCoreTypeAIC,
};

enum ParamType : int8_t {
  kParamTypeUnknown = 0,
  kParamTypeRequired,
  kParamTypeOptional,
  kParamTypeDynamic,
};

inline CoreType StrToCoreType(const std::string &str) {
  if (str == kCoreTypeStrAIV) {
    return kCoreTypeAIV;
  }

  if (str == kCoreTypeStrAIC) {
    return kCoreTypeAIC;
  }

  MSOP_LOG(ERROR) << "Unknown core type: " << str;
  return kCoreTypeUnknown;
}

inline ParamType StrToParamType(const std::string &str) {
  if (str == kParamTypeStrRequired) {
    return kParamTypeRequired;
  }

  if (str == kParamTypeStrOptional) {
    return kParamTypeOptional;
  }

  MSOP_LOG(ERROR) << "Unknown param type: " << str;
  return kParamTypeUnknown;
}

inline DataType StrToDataType(const std::string &str) {
  static const std::unordered_map<std::string, DataType> kStrToDataTypeMap = {
    {kDtypeStrFloat32, kTypeFloat32},     {kDtypeStrFloat16, kTypeFloat16},
    {kDtypeStrInt8, kTypeInt8},           {kDtypeStrInt16, kTypeInt16},
    {kDtypeStrInt32, kTypeInt32},         {kDtypeStrInt64, kTypeInt64},
    {kDtypeStrUint8, kTypeUint8},         {kDtypeStrUint16, kTypeUint16},
    {kDtypeStrUint32, kTypeUint32},       {kDtypeStrUint64, kTypeUint64},
    {kDtypeStrBool, kTypeBool},           {kDtypeStrDouble, kTypeFloat64},
    {kDtypeStrBf16, kTypeBF16},           {kDtypeStrBfloat16, kTypeBF16},
    {kDtypeStrComplex64, kTypeComplex64}, {kDtypeStrComplex128, kTypeComplex128},
  };

  auto iter = kStrToDataTypeMap.find(str);
  if (iter == kStrToDataTypeMap.end()) {
    MSOP_LOG(ERROR) << "Unkonw dtype str: " << str;
    return kTypeUnknown;
  }

  return iter->second;
};

inline TensorFormat StrToFormat(const std::string &str) {
  static const std::unordered_map<std::string, TensorFormat> kStrToFormatMap = {
    {kFormatStrNCHW, kFormatNCHW},       {kFormatStrNHWC, kFormatNHWC},           {kFormatStrND, kFormatND},
    {kFormatStrNC1HWC0, kFormatNC1HWC0}, {kFormatStrFRACTAL_Z, kFormatFRACTAL_Z},
  };

  auto iter = kStrToFormatMap.find(str);
  if (iter == kStrToFormatMap.end()) {
    MSOP_LOG(ERROR) << "Unkonw format str: " << str;
    return kFormatUnknown;
  }

  return iter->second;
}

struct ObjectInfo {
  std::string obejct_file_name;
  std::string core_type;
  std::string magic;
  int32_t simplified_key_mode;
  std::vector<std::string> simplified_keys;
  std::vector<DataType> input_dtypes;
  std::vector<TensorFormat> input_formats;
  std::vector<ParamType> input_param_types;
  std::vector<DataType> output_dtypes;
  std::vector<TensorFormat> output_formats;
  std::vector<ParamType> output_param_types;
};

class HpholKernelLoader {
 public:
  HpholKernelLoader();
  ~HpholKernelLoader() = default;

  static HpholKernelLoader &GetInstance() {
    static HpholKernelLoader object_kernel_loader;
    return object_kernel_loader;
  }

  std::string BuildSimplifiedKey(const InputsDescList &inputs_ii, const OutputsDescList &outputs_ii,
                                 const std::string &kernel_name) const;
  void Init();
  std::string GetObjectFileBySimplifiedKey(const std::string &simplified_key) const;
  InOutDtypesList GetInOutDtypesByKernelName(const std::string &kernel_name) const;
  InOutIndicesType GetInOutOptionalIndices(const std::string &kernel_name) const;

 private:
  std::unordered_map<std::string, std::vector<std::string>> CollectJsons(const std::string &path);
  void ParseJsons(const std::unordered_map<std::string, std::vector<std::string>> &json_infos);
  void ParseObjectInfo(const std::string &file_name);
  void BuildAcmeSimplifiedKeyMap(const std::string &kernel_name, const std::string &file_name,
                                 const ObjectInfo &object_info);
  inline void InsertMap(const std::string &kernel_name, const ObjectInfo &object_info) {
    if (object_infos_.count(kernel_name) == 0) {
      object_infos_[kernel_name] = std::vector<ObjectInfo>{object_info};
    } else {
      object_infos_[kernel_name].emplace_back(object_info);
    }
  }

  std::unordered_map<std::string, std::vector<ObjectInfo>> object_infos_;
  std::unordered_map<std::string, std::string> simplified_key_to_object_file_map_;
  std::unordered_map<std::string, InOutIndicesType> optional_args_indices_;
};

}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_LOADER_OBJECT_KERNEL_LOADER_H_