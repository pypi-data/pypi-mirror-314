/*
 * Copyright (c) 2024 Huawei Technologies Co., Ltd.
 * AscendOpCommonLib is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *          http://license.coscl.org.cn/MulanPSL2
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 */
#ifndef COMMON_RT_MEMORY_MEMORY_H
#define COMMON_RT_MEMORY_MEMORY_H
#include "asdops/utils/rt/base/types.h"
#ifdef __cplusplus
extern "C" {
#endif
namespace AsdOps {
int AsdRtMemMallocDevice(void **devPtr, uint64_t size, AsdRtMemType memType);
int AsdRtMemFreeDevice(void *devPtr);
int AsdRtMemMallocHost(void **hostPtr, uint64_t size);
int AsdRtMemFreeHost(void *hostPtr);
int AsdRtMemCopy(void *dstPtr, uint64_t dstLen, const void *srcPtr, uint64_t srcLen, AsdRtMemCopyType copyType);
int AsdRtMemCopyAsync(void *dstPtr, uint64_t dstLen, const void *srcPtr, uint64_t srcLen, AsdRtMemCopyType copyType,
                      void *stream);
int AsdRtMemSetAsync(void *dstPtr, uint64_t destMax, uint32_t value, uint64_t count, void *stream);
int AsdRtIpcSetMemoryName(const void *ptr, uint64_t byteCount, const char *name, uint32_t len);
int AsdRtIpcOpenMemory(void **ptr, const char *name);
int AsdRtSetIpcMemPid(const char *name, int32_t pid[], int num);
}
#ifdef __cplusplus
}
#endif
#endif