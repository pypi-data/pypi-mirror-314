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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ASD_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ASD_UTILS_H_

#include "asdops/types.h"
#include "utils/log/log.h"
#include "acme/include/base_type.h"
#include "acme/src/utils/comm_utils.h"

namespace mindspore {
namespace acme {
constexpr size_t kIdx0 = 0;
constexpr size_t kIdx1 = 1;
constexpr size_t kIdx2 = 2;
constexpr size_t kIdx3 = 3;
constexpr int64_t DEFAULT_ALIGN = 16;
constexpr int64_t DEFAULT_INT8_ALIGN = 32;

using DIMS = AsdOps::SVector<int64_t>;

inline DIMS NdToNz(const DIMS &inDims, const DataType &dtype) {
  DIMS auxDims{0, 0, 0, 0};
  DIMS nzDims{0, 0, 0, 0};
  DIMS realInDims{0, 0, 0};
  if (inDims.size() == 1) {
    realInDims[kIdx0] = 1;
    realInDims[kIdx1] = 1;
    realInDims[kIdx2] = inDims[kIdx0];
  } else if (inDims.size() == 2) {
    realInDims[kIdx0] = 1;
    realInDims[kIdx1] = inDims[kIdx0];
    realInDims[kIdx2] = inDims[kIdx1];
  } else if (inDims.size() == 3) {
    realInDims[kIdx0] = inDims[kIdx0];
    realInDims[kIdx1] = inDims[kIdx1];
    realInDims[kIdx2] = inDims[kIdx2];
  } else {
    realInDims[kIdx0] = inDims[kIdx0];
    realInDims[kIdx1] = inDims[kIdx1];
    realInDims[kIdx2] = inDims[kIdx2] * inDims[kIdx3];
  }

  int64_t nzAlign = DEFAULT_ALIGN;
  if (dtype == DataType::kTypeInt8) {
    nzAlign = DEFAULT_INT8_ALIGN;
  }

  // inference aux dims: [N, H, W] -> [N, H', W'/16, 16]
  auxDims[kIdx0] = realInDims[kIdx0];
  auxDims[kIdx1] = UpRound(realInDims[kIdx1], DEFAULT_ALIGN);
  auxDims[kIdx2] = UpRound(realInDims[kIdx2], nzAlign) / nzAlign;
  auxDims[kIdx3] = nzAlign;

  // inference output dims: [N, H', W'/16, 16] -> [N, W'/16, H', 16]
  nzDims[kIdx0] = auxDims[kIdx0];
  nzDims[kIdx1] = auxDims[kIdx2];
  nzDims[kIdx2] = auxDims[kIdx1];
  nzDims[kIdx3] = auxDims[kIdx3];
  return nzDims;
}

inline DIMS ConvertStandardNdDims(const DIMS &inDims) {
  DIMS dims{0, 0, 0};
  if (inDims.size() == 2) {
    dims[kIdx0] = 1;
    dims[kIdx1] = inDims[kIdx0];
    dims[kIdx2] = inDims[kIdx1];
  } else {
    dims[0] = inDims[kIdx0];
    dims[1] = inDims[kIdx1];
    dims[2] = inDims[kIdx2];
    if (inDims.size() == 4) {
      dims[2] *= inDims[kIdx3];
    }
  }
  return dims;
}

inline AsdOps::TensorDType ToAsdType(DataType type) {
  switch (type) {
    // float data type
    case DataType::kTypeBF16:
      return AsdOps::TENSOR_DTYPE_BF16;
    case DataType::kTypeFloat16:
      return AsdOps::TENSOR_DTYPE_FLOAT16;
    case DataType::kTypeFloat32:
      return AsdOps::TENSOR_DTYPE_FLOAT;
    case DataType::kTypeFloat64:
      return AsdOps::TENSOR_DTYPE_DOUBLE;
    // uint data type
    case DataType::kTypeUint8:
      return AsdOps::TENSOR_DTYPE_UINT8;
    case DataType::kTypeUint16:
      return AsdOps::TENSOR_DTYPE_UINT16;
    case DataType::kTypeUint32:
      return AsdOps::TENSOR_DTYPE_UINT32;
    case DataType::kTypeUint64:
      return AsdOps::TENSOR_DTYPE_UINT64;
    // int data type
    case DataType::kTypeInt8:
      return AsdOps::TENSOR_DTYPE_INT8;
    case DataType::kTypeInt16:
      return AsdOps::TENSOR_DTYPE_INT16;
    case DataType::kTypeInt32:
      return AsdOps::TENSOR_DTYPE_INT32;
    case DataType::kTypeInt64:
      return AsdOps::TENSOR_DTYPE_INT64;
    // complex data type
    case DataType::kTypeComplex64:
      return AsdOps::TENSOR_DTYPE_COMPLEX64;
    case DataType::kTypeComplex128:
      return AsdOps::TENSOR_DTYPE_COMPLEX128;
    // other data type
    case DataType::kTypeString:
      return AsdOps::TENSOR_DTYPE_STRING;
    case DataType::kTypeBool:
      return AsdOps::TENSOR_DTYPE_BOOL;
    case DataType::kTypeNone:
      return AsdOps::TENSOR_DTYPE_UNDEFINED;
    default:
      MSOP_LOG(EXCEPTION) << "Unsupported type: " << type;
      return AsdOps::TENSOR_DTYPE_UNDEFINED;
  }
}

inline AsdOps::TensorFormat ToAsdFormat(TensorFormat format) {
  switch (format) {
    case TensorFormat::kFormatUnknown:
      return AsdOps::TENSOR_FORMAT_UNDEFINED;
    case TensorFormat::kFormatNCHW:
      return AsdOps::TENSOR_FORMAT_NCHW;
    case TensorFormat::kFormatND:
      return AsdOps::TENSOR_FORMAT_ND;
    case TensorFormat::kFormatNHWC:
      return AsdOps::TENSOR_FORMAT_NHWC;
    case TensorFormat::kFormatFRACTAL_NZ:
      return AsdOps::TENSOR_FORMAT_FRACTAL_NZ;
    default:
      MSOP_LOG(EXCEPTION) << "Unsupported format: " << format;
      return AsdOps::TENSOR_FORMAT_UNDEFINED;
  }
}

inline void ToAsdDimsInplace(const ShapeInfo &shape, const DataType &dtype, const TensorFormat &format, DIMS *dims) {
  dims->resize(shape.size());
  for (auto i = 0; i < shape.size(); i++) {
    dims->at(i) = shape[i];
  }

  if (format == TensorFormat::kFormatFRACTAL_NZ) {
    *dims = NdToNz(*dims, dtype);
    MSOP_LOG(DEBUG) << " nd_shape = " << shape << ", nz_shape = " << *dims;
  }
}

inline DIMS ToAsdDims(const ShapeInfo &shape, const DataType &dtype, const TensorFormat &format) {
  DIMS asd_dims;
  ToAsdDimsInplace(shape, dtype, format, &asd_dims);
  return asd_dims;
}
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_UTILS_ASD_UTILS_H_