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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_BUTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_BUTILS_H_
#include <vector>
#include <iostream>
#include "acl/acl.h"
#include "acl/acl_rt.h"
#include "acme/src/ops/llama/kernel/tiling_data.h"
#include "acme/src/ops/llama/tensor.h"

constexpr float kFloatMSEC = 1000.0f;
const int USEC = 1000000;
const int MSEC = 1000;

#define CUBE_CORE_NUM_910B1 24
#define VEC_CORE_NUM_910B1 48
#define CUBE_CORE_NUM_910B2 24
#define VEC_CORE_NUM_910B2 48
#define CUBE_CORE_NUM_910B4 20
#define VEC_CORE_NUM_910B4 40

namespace mindspore::acme {

void *MallocDevice(size_t size);
void FreeDevice(void *ptr);
int SyncDevice(void *stream);
void PrintFp16(void *x, size_t elem_num, void *stream);
void PrintFp32(void *x, size_t elem_num, void *stream);
void PrintInt32(void *x, size_t elem_num, void *stream);
void *CreateStream(void *context);
void *CreateContext(int32_t deviceId = 0);
void *MallocCopy(void *src, size_t size);
int InitAcl(int device_id);
int initCoresNum(int device_id);
int FinalizeAcl(int device_id);
void DestroyStream(void *stream);
void DestroyCtx(void *context);
void SetContext(void *ctx);
void printChecksumFp32(void *x, size_t elem_num, void *stream);
void printChecksumInt32(void *x, size_t elem_num, void *stream);
void PrintInfo(void *stream);
template <typename T>
void printVector(void *x, int elem_num, void *q);
void printChecksumFp16(void *x, size_t elem_num, void *stream);
void PrintFp16Host(void *x, size_t elem_num, void *stream);
void CopyDTD(void *dst, void *src, size_t size);
void CopyHTD(void *dst, void *src, size_t size);
void CopyDTH(void *dst, void *src, size_t size);
void CopyDTHAsync(void *dst, void *src, size_t size, void *stream);
int MemGetInfo(size_t *free, size_t *total);
size_t getConsumeMemory();
uint64_t GetTimeUs();
void SaveToFile(const std::string &name, void *vec, int elem, void *stream);
void vectorCheckNanOrInf(void *x, int elem_num, char *tensor_name, void *stream);
void printVectorChecksum(void *x, int elem_num, void *q);
void saveTensor(char *name, int cnt, void *tensor, int size);
std::vector<int64_t> calcStride(const std::vector<int64_t> &shape);
int getVecNum();
int getCubeNum();
void CopyHostFp32ToDeviceFp16(void *src, void **dst_ptr, size_t elem_num, void *stream);
void CopyHostFp32ToDeviceFp32(void *src, void **dst_ptr, size_t elem_num, void *stream);
void CopyHostFp16ToDeviceFp16(void *src, void **dst_ptr, size_t elem_num, void *stream);
void CopyHostInt8ToDeviceInt8(void *src, void **dst_ptr, size_t elem_num, void *stream);

void CopyHostFp16ToDeviceFp32(void *src, void **dst_ptr, size_t elem_num, void *stream);
void CopyDeviceFp16ToHostFp32(void *src, void *dst, size_t elem_num, void *stream);
void CopyDeviceFp32ToHostFp32(void *src, void *dst, size_t elem_num, void *stream);
void CopyDeviceFp16ToHostFp16(void *src, void *dst, size_t elem_num, void *stream);
void CopyDeviceFp32ToHostFp16(void *src, void *dst, size_t elem_num, void *stream);
void CopyDeviceInt32oHostInt64(void *src, void *dst, size_t elem_num, void *stream);
void CopyDeviceInt8ToHostInt8(void *src, void *dst, size_t elem_num, void *stream);

void CopyDeviceInt32ToHostInt32(void *src, void *dst, size_t elem_num, void *stream);
void CopyLlamaHTD(void *input, void *bvl, void *mode, void **dst_input, size_t batch_size, size_t seq, void *q);
void CompareTensorsFp16(aclFloat16 *data1, aclFloat16 *data2, int token_num, int token_size, void *stream);
void CompareTensorsInt32(int *data1, int *data2, int token_num, int token_size, void *stream);
}  // namespace mindspore::acme
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_BUTILS_H_
