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

#ifndef __SRC_ACME_SRC_OPS_ADD_LAYER_NORM_KERNEL_ADD_LAYER_NORM_SPECIAL_REDUCE_H_
#define __SRC_ACME_SRC_OPS_ADD_LAYER_NORM_KERNEL_ADD_LAYER_NORM_SPECIAL_REDUCE_H_

#include "add_layer_norm_base.h"

template <typename T_X1, typename T_X2, typename T_GAMMA, typename T, int TILING_KEY, int BUFFER_NUM = 1>
class KernelAddLayerNormNormalSpecialReduce {
#define IS_ADDITIONAL_OUTPUT_ENABLE ((TILING_KEY % 1000) / 100 == 1)
#define IS_NORMAL_BIG_N_CASE_R ((TILING_KEY % 100) / 10 == 8)
#define IS_BIAS_BROADCAST ((TILING_KEY % 10) == 2)

 public:
  __aicore__ inline KernelAddLayerNormNormalSpecialReduce(TPipe *pipe) { Ppipe = pipe; }

  __aicore__ inline uint32_t CEIL_DIV(uint32_t x, uint32_t y) {
    if (y > 0) {
      return (x + y - 1) / y;
    }
    return 0;
  }

  __aicore__ inline uint32_t ROUND_UP32(uint32_t x) { return (x + ONE_BLK_SIZE - 1) / ONE_BLK_SIZE * ONE_BLK_SIZE; }

  __aicore__ inline uint32_t BlockAlign(uint32_t x, uint32_t blockElem) {
    if (blockElem > 0) {
      return (x + blockElem - 1) / blockElem * blockElem;
    }
    return 0;
  }

  __aicore__ inline uint32_t MIN(uint32_t x, uint32_t y) { return x < y ? x : y; }

  __aicore__ inline uint32_t MAX(uint32_t x, uint32_t y) { return x > y ? x : y; }

  __aicore__ inline void Init(__gm__ uint8_t *x1, __gm__ uint8_t *x2, __gm__ uint8_t *gamma, __gm__ uint8_t *beta,
                              __gm__ uint8_t *bias, __gm__ uint8_t *y, __gm__ uint8_t *mean, __gm__ uint8_t *rstd,
                              __gm__ uint8_t *x, __gm__ uint8_t *workspace, uint32_t numCore_, uint32_t numLastDim_,
                              uint32_t numFirstDim_, uint32_t nlFirstDimPerCore_, uint32_t lFirstDimPerCore_,
                              uint32_t firstDimPerTime_, uint32_t lastDimPerTime_, float eps_, float aveNum_,
                              uint32_t colMoveCnt_, uint32_t colTail_, uint32_t workspace_size) {
    numCore = numCore_;
    numLastDim = numLastDim_;
    numFirstDim = numFirstDim_;
    notLastFirstDimPerCore = nlFirstDimPerCore_;
    lFirstDimPerCore = lFirstDimPerCore_;
    firstDimPerTime = firstDimPerTime_;
    lastDimPerTime = lastDimPerTime_;
    aveNum = aveNum_;
    eps = eps_;
    colMoveCnt = colMoveCnt_;
    colTail = colTail_;
    if (block_idx != numCore - 1) {
      rowWork = notLastFirstDimPerCore;
      rowStep = firstDimPerTime;
    } else {
      rowWork = lFirstDimPerCore;
      rowStep = MIN(firstDimPerTime, rowWork);
    }
    rowTail_ = (rowWork % rowStep == 0) ? rowStep : (rowWork % rowStep);
    gmOffset_ = notLastFirstDimPerCore * numLastDim;
    x1Gm.SetGlobalBuffer((__gm__ T *)(x1) + block_idx * gmOffset_);
    x2Gm.SetGlobalBuffer((__gm__ T *)(x2) + block_idx * gmOffset_);
    gammaGm.SetGlobalBuffer((__gm__ T *)gamma);
    betaGm.SetGlobalBuffer((__gm__ T *)beta);
    yGm.SetGlobalBuffer((__gm__ T *)(y) + block_idx * gmOffset_);
    // mean/rstd always output fp32
    meanGm.SetGlobalBuffer((__gm__ float *)mean + block_idx * notLastFirstDimPerCore);
    rstdGm.SetGlobalBuffer((__gm__ float *)rstd + block_idx * notLastFirstDimPerCore);
    xGm.SetGlobalBuffer((__gm__ T *)(x) + block_idx * gmOffset_);
    if constexpr (IS_BIAS_BROADCAST) {
      biasGm.SetGlobalBuffer((__gm__ T *)bias);
    }

    numLastDimAligned = numLastDim;
    if (ROUND_UP32(numLastDim * sizeof(T)) != numLastDim * sizeof(T)) {
      lastDimPad = true;
      numLastDimAligned = ROUND_UP32(numLastDim * sizeof(T)) / sizeof(T);
    }

    Ppipe->InitBuffer(x1x2Que, BUFFER_NUM, ROUND_UP32(2 * rowStep * numLastDimAligned * sizeof(T)));
    Ppipe->InitBuffer(yQue, BUFFER_NUM, ROUND_UP32(rowStep * numLastDimAligned * sizeof(T)));
    Ppipe->InitBuffer(betaBuf, ROUND_UP32(numLastDimAligned * sizeof(float)));
    Ppipe->InitBuffer(gammaBuf, ROUND_UP32(numLastDimAligned * sizeof(float)));
    if constexpr (IS_BIAS_BROADCAST) {
      Ppipe->InitBuffer(biasBuf, ROUND_UP32(numLastDim * sizeof(T)));
    }

    Ppipe->InitBuffer(xBufFp32, ROUND_UP32(rowStep * numLastDimAligned * sizeof(float)));
    Ppipe->InitBuffer(zBufFp32, ROUND_UP32(rowStep * numLastDimAligned * sizeof(float)));
#if __CCE_AICORE__ == 220
    uint32_t brcbRowStep = BlockAlign(rowStep, BRCB_BROADCAST_NUMBER);
    Ppipe->InitBuffer(yBufFp32, ROUND_UP32(brcbRowStep * ELEM_PER_REP_FP32 * sizeof(float)));
#else
    Ppipe->InitBuffer(yBufFp32, ROUND_UP32(rowStep * ELEM_PER_REP_FP32 * sizeof(float)));
#endif

#if __CCE_AICORE__ != 220
    Ppipe->InitBuffer(orBufINT16, 16 * sizeof(int16_t));  // one block

    if constexpr (IS_NORMAL_BIG_N_CASE_R) {
      Ppipe->InitBuffer(transposeSrcBuf, ROUND_UP32(16 * 16 * 8 * sizeof(half)));
      Ppipe->InitBuffer(transposeDstBuf, ROUND_UP32(16 * 16 * 8 * sizeof(half)));
    }
#endif

#if OUTPUT_MEAN_RSTD == 1
    Ppipe->InitBuffer(meanQue, BUFFER_NUM, ROUND_UP32(rowStep * sizeof(float)));
    Ppipe->InitBuffer(rstdQue, BUFFER_NUM, ROUND_UP32(rowStep * sizeof(float)));
#endif
  }

  __aicore__ inline void Process() {
    int32_t rowMoveCnt = CEIL_DIV(rowWork, rowStep);

    DataCopyPadParams padParams;
    if (lastDimPad) {
      padParams.isPad = true;
      padParams.paddingValue = 0;
      padParams.rightPadding = numLastDimAligned - numLastDim;
    }

    LocalTensor<float> betaLocal = betaBuf.template Get<float>();
    LocalTensor<float> gammaLocal = gammaBuf.template Get<float>();

    if constexpr (is_same<float, T>::value) {
      DataCopyEx(betaLocal, betaGm, numLastDim);
      DataCopyEx(gammaLocal, gammaGm, numLastDim);
    } else {
      auto betaLocalHalf = betaLocal.ReinterpretCast<T>();
      auto gammaLocalHalf = gammaLocal.ReinterpretCast<T>();
      DataCopyEx(betaLocalHalf[numLastDimAligned], betaGm, numLastDim);
      DataCopyEx(gammaLocalHalf[numLastDimAligned], gammaGm, numLastDim);
    }

    LocalTensor<T> biasLocal;
    if constexpr (IS_BIAS_BROADCAST) {
      biasLocal = biasBuf.template Get<T>();
      DataCopyEx(biasLocal, biasGm, numLastDim);
    }

    uint32_t gmOffset = 0;
    uint32_t elementCount = numLastDimAligned * rowStep;

    {
      LocalTensor<T> x1x2LocalIn = x1x2Que.template AllocTensor<T>();
      DataCopyEx(x1x2LocalIn[0], x1Gm[gmOffset], numLastDim, rowStep, padParams);
      DataCopyEx(x1x2LocalIn[elementCount], x2Gm[gmOffset], numLastDim, rowStep, padParams);
      x1x2Que.EnQue(x1x2LocalIn);
      auto x1x2Local = x1x2Que.template DeQue<T>();

      if constexpr (!is_same<T, float>::value) {
        Cast(gammaLocal, gammaLocal.ReinterpretCast<T>()[numLastDimAligned], RoundMode::CAST_NONE, numLastDim);
        Cast(betaLocal, betaLocal.ReinterpretCast<T>()[numLastDimAligned], RoundMode::CAST_NONE, numLastDim);
      }

      if constexpr (IS_BIAS_BROADCAST) {
        CopyInAndAddBroadCast(rowStep, elementCount, biasLocal, x1x2Local);
      } else {
        CopyIn(rowStep, elementCount, x1x2Local, padParams);
      }
      CopyOutAdditionalOutput(0, rowStep);
      if constexpr (IS_NORMAL_BIG_N_CASE_R) {
        PrecisionComputeBigN(rowStep, gammaLocal, betaLocal);
      } else {
        PrecisionCompute(rowStep, gammaLocal, betaLocal, elementCount);
      }
      CopyOut(0, rowStep);
      gmOffset += rowStep * numLastDim;
    }
    for (int32_t rowIdx = 1; rowIdx < rowMoveCnt - 1; ++rowIdx) {
      LocalTensor<T> x1x2LocalIn = x1x2Que.template AllocTensor<T>();
      DataCopyEx(x1x2LocalIn[0], x1Gm[gmOffset], numLastDim, rowStep, padParams);
      DataCopyEx(x1x2LocalIn[elementCount], x2Gm[gmOffset], numLastDim, rowStep, padParams);
      x1x2Que.EnQue(x1x2LocalIn);
      auto x1x2Local = x1x2Que.template DeQue<T>();
      if constexpr (IS_BIAS_BROADCAST) {
        CopyInAndAddBroadCast(rowStep, elementCount, biasLocal, x1x2Local);
      } else {
        CopyIn(rowStep, elementCount, x1x2Local, padParams);
      }

      CopyOutAdditionalOutput(rowIdx, rowStep);
      if constexpr (IS_NORMAL_BIG_N_CASE_R) {
        PrecisionComputeBigN(rowStep, gammaLocal, betaLocal);
      } else {
        PrecisionCompute(rowStep, gammaLocal, betaLocal, elementCount);
      }
      CopyOut(rowIdx, rowStep);
      gmOffset += rowStep * numLastDim;
    }
    {
      auto rowIdx = rowMoveCnt - 1;
      if (rowIdx > 0) {
        elementCount = numLastDimAligned * rowTail_;

        LocalTensor<T> x1x2LocalIn = x1x2Que.template AllocTensor<T>();
        DataCopyEx(x1x2LocalIn[0], x1Gm[gmOffset], numLastDim, rowTail_, padParams);
        DataCopyEx(x1x2LocalIn[elementCount], x2Gm[gmOffset], numLastDim, rowTail_, padParams);
        x1x2Que.EnQue(x1x2LocalIn);
        auto x1x2Local = x1x2Que.template DeQue<T>();
        if constexpr (IS_BIAS_BROADCAST) {
          CopyInAndAddBroadCast(rowTail_, elementCount, biasLocal, x1x2Local);
        } else {
          CopyIn(rowTail_, elementCount, x1x2Local, padParams);
        }

        CopyOutAdditionalOutput(rowIdx, rowTail_);
        if constexpr (IS_NORMAL_BIG_N_CASE_R) {
          PrecisionComputeBigN(rowTail_, gammaLocal, betaLocal);
        } else {
          PrecisionCompute(rowTail_, gammaLocal, betaLocal, elementCount);
        }
        CopyOut(rowIdx, rowTail_);
      }
    }
  }

 private:
  __aicore__ inline void CopyInAndAddBroadCast(int32_t rowCount, uint32_t elementCount, LocalTensor<T> &biasLocal,
                                               LocalTensor<T> &x1x2Local) {
    LocalTensor<float> addBufLocal = zBufFp32.Get<float>();
    LocalTensor<float> xBufLocal = xBufFp32.Get<float>();

    auto x1Local = x1x2Local[0];
    auto x2Local = x1x2Local[elementCount];

    // Use add as
    if constexpr (is_same<float, T>::value) {
      Add(addBufLocal, x2Local, x1Local, elementCount);
      pipe_barrier(PIPE_V);
      for (int i = 0; i < rowCount; i++) {
        Add(addBufLocal[i * numLastDimAligned], biasLocal, addBufLocal[i * numLastDimAligned], numLastDim);
      }
      pipe_barrier(PIPE_V);
    } else {
      Cast(addBufLocal, x1Local, RoundMode::CAST_NONE, elementCount);
      Cast(xBufLocal, x2Local, RoundMode::CAST_NONE, elementCount);
      pipe_barrier(PIPE_V);
      Add(xBufLocal, addBufLocal, xBufLocal, elementCount);
      Cast(x1x2Local.template ReinterpretCast<float>(), biasLocal, RoundMode::CAST_NONE, numLastDim);
      pipe_barrier(PIPE_V);
      for (int i = 0; i < rowCount; i++) {
        Add(addBufLocal[i * numLastDimAligned], x1x2Local.template ReinterpretCast<float>(),
            xBufLocal[i * numLastDimAligned], numLastDim);
      }
      pipe_barrier(PIPE_V);
    }
    x1x2Que.FreeTensor(x1x2Local);
  }

  __aicore__ inline void CopyIn(int32_t rowCount, uint32_t elementCount, LocalTensor<T> &x1x2Local,
                                const DataCopyPadParams &padParams = {}) {
    auto x1Local = x1x2Local[0];
    auto x2Local = x1x2Local[elementCount];

    LocalTensor<float> xLocalFp32 = xBufFp32.Get<float>();
    LocalTensor<float> addBufLocal = zBufFp32.Get<float>();

    // Use add as
    if constexpr (is_same<float, T>::value) {
      Add(addBufLocal, x2Local, x1Local, elementCount);
      pipe_barrier(PIPE_V);
    } else {
      Cast(addBufLocal, x1Local, RoundMode::CAST_NONE, elementCount);
      Cast(xLocalFp32, x2Local, RoundMode::CAST_NONE, elementCount);
      pipe_barrier(PIPE_V);
      Add(addBufLocal, addBufLocal, xLocalFp32, elementCount);
      pipe_barrier(PIPE_V);
    }
    x1x2Que.FreeTensor(x1x2Local);
  }

  __aicore__ inline void CopyOutAdditionalOutput(int32_t procId, int32_t rowCount) {
    if constexpr (IS_ADDITIONAL_OUTPUT_ENABLE) {
      LocalTensor<float> addBufLocal = zBufFp32.Get<float>();
      uint32_t gmOffset = procId * rowStep * numLastDim;
      auto elementCount = numLastDimAligned * rowCount;
      auto xLocal = yQue.template AllocTensor<T>();
      if constexpr (is_same<T, float>::value) {
        Adds(xLocal, addBufLocal, ZERO, elementCount);
      } else if constexpr (is_same<T, half>::value) {
        Cast(xLocal, addBufLocal, RoundMode::CAST_NONE, elementCount);
      } else {
        Cast(xLocal, addBufLocal, RoundMode::CAST_RINT, elementCount);
      }
      pipe_barrier(PIPE_V);
      yQue.template EnQue<T>(xLocal);

      auto x = yQue.template DeQue<T>();
      DataCopyEx(xGm[gmOffset], x, numLastDim, rowCount);
      yQue.FreeTensor(x);
    }
  }

  __aicore__ inline void PrecisionCompute(int32_t nums, LocalTensor<float> &gammaLocal, LocalTensor<float> &betaLocal,
                                          uint32_t elementCount) {
    event_t eventSV = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::S_V));
    event_t eventVS = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::V_S));

#if OUTPUT_MEAN_RSTD == 1
    LocalTensor<float> meanLocal = meanQue.template AllocTensor<float>();
    LocalTensor<float> rstdLocal = rstdQue.template AllocTensor<float>();
#endif
    LocalTensor<float> xLocalFp32 = xBufFp32.Get<float>();
    LocalTensor<float> yLocalFp32 = yBufFp32.Get<float>();  // for reduce
    LocalTensor<float> zLocalFp32 = zBufFp32.Get<float>();

    // 1.1. mean process: 1/N * x_sum
    Muls(xLocalFp32, zLocalFp32, aveNum, elementCount);
    // 1.2. init buffer for reduce
    Duplicate(yLocalFp32, ZERO, nums * ELEM_PER_REP_FP32);
    pipe_barrier(PIPE_V);

    // 2. mean end: reduce(1/N * x_sum)
    const uint32_t tailCount = numLastDim % ELEM_PER_REP_FP32;
    const uint32_t repeat = nums;  // repeat < 255 * 8 = 2040
    const uint8_t repStride = numLastDimAligned / FLOAT_BLOCK_ELEM;
    ReduceSumForSmallReduceDim(xLocalFp32, xLocalFp32, yLocalFp32, numLastDimAligned, numLastDim, tailCount, repeat,
                               repStride);

    // 3. rstd process: x - mean
    set_flag(PIPE_V, PIPE_S, eventVS);
    wait_flag(PIPE_V, PIPE_S, eventVS);
    for (int32_t rid = 0; rid < nums; ++rid) {
      auto roundOffset = rid * numLastDimAligned;

      auto meanTemp = xLocalFp32.GetValue(rid);
#if OUTPUT_MEAN_RSTD == 1
      meanLocal.SetValue(rid, meanTemp);
#endif
      set_flag(PIPE_S, PIPE_V, eventSV);
      wait_flag(PIPE_S, PIPE_V, eventSV);
      Adds(zLocalFp32[roundOffset], zLocalFp32[roundOffset], meanTemp * -1, numLastDim);
    }
    pipe_barrier(PIPE_V);

    // 4. rstd process: (x - mean) ^ 2
    Mul(xLocalFp32, zLocalFp32, zLocalFp32, elementCount);
    pipe_barrier(PIPE_V);

    // 5. rstd process: reduce( 1 / N * (x - mean) ^ 2 )
    Muls(xLocalFp32, xLocalFp32, aveNum, elementCount);
    pipe_barrier(PIPE_V);
    Duplicate(yLocalFp32, ZERO, nums * ELEM_PER_REP_FP32);
    pipe_barrier(PIPE_V);
    ReduceSumForSmallReduceDim(xLocalFp32, xLocalFp32, yLocalFp32, numLastDimAligned, numLastDim, tailCount, repeat,
                               repStride);
    pipe_barrier(PIPE_V);

    // 6. rstd end: 1 / sqrt( 1 / N * reduce( (x - mean) ^ 2 ) )
    Adds(xLocalFp32, xLocalFp32, eps, repeat);
    pipe_barrier(PIPE_V);
    Sqrt(xLocalFp32, xLocalFp32, repeat);
    Duplicate(yLocalFp32, float(1), repeat);
    pipe_barrier(PIPE_V);
    Div(xLocalFp32, yLocalFp32, xLocalFp32, repeat);

    // 7. y process: (x - mean) / rstd
    set_flag(PIPE_V, PIPE_S, eventVS);
    wait_flag(PIPE_V, PIPE_S, eventVS);
    for (int32_t rid = 0; rid < nums; ++rid) {
      auto roundOffset = rid * numLastDimAligned;

      float rstdTmp = xLocalFp32.GetValue(rid);
#if OUTPUT_MEAN_RSTD == 1
      rstdLocal.SetValue(rid, rstdTmp);
#endif
      set_flag(PIPE_S, PIPE_V, eventSV);
      wait_flag(PIPE_S, PIPE_V, eventSV);
      Muls(zLocalFp32[roundOffset], zLocalFp32[roundOffset], rstdTmp, numLastDim);
    }
    pipe_barrier(PIPE_V);

    // 8. y = (x - mean) / rstd * beta + gamma
    LocalTensor<T> yLocal = yQue.template AllocTensor<T>();
    if constexpr (!is_same<T, float>::value) {
      for (int32_t rid = 0; rid < nums; ++rid) {
        Mul(zLocalFp32[rid * numLastDimAligned], zLocalFp32[rid * numLastDimAligned], gammaLocal, numLastDim);
      }
      pipe_barrier(PIPE_V);
      for (int32_t rid = 0; rid < nums; ++rid) {
        Add(zLocalFp32[rid * numLastDimAligned], zLocalFp32[rid * numLastDimAligned], betaLocal, numLastDim);
      }
      pipe_barrier(PIPE_V);

      if constexpr (is_same<T, half>::value) {
        Cast(yLocal, zLocalFp32, RoundMode::CAST_NONE, elementCount);
      } else {
        Cast(yLocal, zLocalFp32, RoundMode::CAST_RINT, elementCount);
      }
    } else {
      for (int32_t rid = 0; rid < nums; ++rid) {
        Mul(zLocalFp32[rid * numLastDimAligned], zLocalFp32[rid * numLastDimAligned], gammaLocal, numLastDim);
      }
      pipe_barrier(PIPE_V);
      for (int32_t rid = 0; rid < nums; ++rid) {
        Add(yLocal[rid * numLastDimAligned], zLocalFp32[rid * numLastDimAligned], betaLocal, numLastDim);
      }
      pipe_barrier(PIPE_V);
    }

#if OUTPUT_MEAN_RSTD == 1
    meanQue.EnQue(meanLocal);
    rstdQue.EnQue(rstdLocal);
#endif
    yQue.EnQue(yLocal);
  }

  __aicore__ inline void PrecisionComputeBigN(int32_t nums, LocalTensor<float> &gammaLocal,
                                              LocalTensor<float> &betaLocal) {
#if __CCE_AICORE__ == 220
    PrecisionComputeBigNBrcb(nums, gammaLocal, betaLocal);
#else
    precisionComputeBigNTranspose(nums, gammaLocal, betaLocal);
#endif
  }

  __aicore__ inline void precisionComputeBigNTranspose(int32_t nums, LocalTensor<float> &gammaLocal,
                                                       LocalTensor<float> &betaLocal) {
    event_t eventSV = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::S_V));
    event_t eventVS = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::V_S));

    LocalTensor<int16_t> orOffsetINT16 = orBufINT16.Get<int16_t>();

    LocalTensor<float> xLocalFp32 = xBufFp32.Get<float>();
    LocalTensor<float> yLocalFp32 = yBufFp32.Get<float>();
    LocalTensor<float> zLocalFp32 = zBufFp32.Get<float>();

    LocalTensor<float> transposeSrcLocal = transposeSrcBuf.Get<float>();
    LocalTensor<float> transposeDstLocal = transposeDstBuf.Get<float>();

    int32_t elementNum = numLastDimAligned * nums;

    // 1.1. mean process: 1/N * x_sum
    Muls(xLocalFp32, zLocalFp32, aveNum, elementNum);
    // 1.2. init buffer for reduce
    Duplicate(yLocalFp32, ZERO, nums * ELEM_PER_REP_FP32);
    pipe_barrier(PIPE_V);

    // 2.1. reducesum
    const uint32_t forCount = numLastDim / ELEM_PER_REP_FP32;
    const uint32_t tailCount = numLastDim % ELEM_PER_REP_FP32;
    const uint32_t repeat = nums;  // repeat < 255 * 8 = 2040
    const uint8_t repStride = numLastDimAligned / FLOAT_BLOCK_ELEM;
    ReduceSumForSmallReduceDim(xLocalFp32, xLocalFp32, yLocalFp32, numLastDimAligned, numLastDim, tailCount, repeat,
                               repStride);
    pipe_barrier(PIPE_V);

    // 2.2. broadcast reducesum value
    InitVAForTranspose((__ubuf__ half *)transposeDstLocal.GetPhyAddr(),
                       (__ubuf__ half *)transposeSrcLocal.GetPhyAddr());
    CCEBroadCastShort((__ubuf__ int16_t *)xLocalFp32.GetPhyAddr(), (__ubuf__ float *)xLocalFp32.GetPhyAddr(),
                      (__ubuf__ int16_t *)transposeDstLocal.GetPhyAddr(),
                      (__ubuf__ int16_t *)transposeSrcLocal.GetPhyAddr(),
                      (__ubuf__ int16_t *)orOffsetINT16.GetPhyAddr(), forCount, tailCount, repeat, repStride);
    pipe_barrier(PIPE_V);

    // 3. rstd process: x - mean
    Sub(zLocalFp32, zLocalFp32, xLocalFp32, elementNum);
    pipe_barrier(PIPE_V);

    // 4. rstd process: (x - mean) ^ 2
    Mul(xLocalFp32, zLocalFp32, zLocalFp32, elementNum);
    pipe_barrier(PIPE_V);

    // 5. rstd process: reduce( 1 / N * (x - mean) ^ 2 )
    Muls(xLocalFp32, xLocalFp32, aveNum, elementNum);
    Duplicate(yLocalFp32, ZERO, nums * ELEM_PER_REP_FP32);
    pipe_barrier(PIPE_V);
    ReduceSumForSmallReduceDim(xLocalFp32, xLocalFp32, yLocalFp32, numLastDimAligned, numLastDim, tailCount, repeat,
                               repStride);
    pipe_barrier(PIPE_V);

    // 6. rstd end: 1 / sqrt( 1 / N * reduce( (x - mean) ^ 2 ) )
    Adds(xLocalFp32, xLocalFp32, eps, nums);
    pipe_barrier(PIPE_V);
    Sqrt(xLocalFp32, xLocalFp32, nums);
    Duplicate(yLocalFp32, (float)1, nums);
    pipe_barrier(PIPE_V);
    Div(xLocalFp32, yLocalFp32, xLocalFp32, nums);
    pipe_barrier(PIPE_V);

    // 7. broadcast reducesum value
    CCEBroadCastShort((__ubuf__ int16_t *)xLocalFp32.GetPhyAddr(), (__ubuf__ float *)xLocalFp32.GetPhyAddr(),
                      (__ubuf__ int16_t *)transposeDstLocal.GetPhyAddr(),
                      (__ubuf__ int16_t *)transposeSrcLocal.GetPhyAddr(),
                      (__ubuf__ int16_t *)orOffsetINT16.GetPhyAddr(), forCount, tailCount, repeat, repStride);
    pipe_barrier(PIPE_V);
    Mul(zLocalFp32, zLocalFp32, xLocalFp32, elementNum);
    pipe_barrier(PIPE_V);

    // 8. y = (x - mean) / rstd * beta + gamma
    LocalTensor<T> yLocal = yQue.template AllocTensor<T>();
    if constexpr (!is_same<T, float>::value) {
      Level0MulFp32Short(zLocalFp32, gammaLocal, zLocalFp32, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);
      Level0AddFp32Short(zLocalFp32, betaLocal, zLocalFp32, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);

      if constexpr (is_same<T, half>::value) {
        Cast(yLocal, zLocalFp32, RoundMode::CAST_NONE, elementNum);
      } else {
        Cast(yLocal, zLocalFp32, RoundMode::CAST_RINT, elementNum);
      }
      pipe_barrier(PIPE_V);
    } else {
      Level0MulFp32Short(yLocal, gammaLocal, zLocalFp32, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);
      Level0AddFp32Short(yLocal, betaLocal, yLocal, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);
    }

    yQue.EnQue(yLocal);
  }

#if __CCE_AICORE__ == 220
  __aicore__ inline void PrecisionComputeBigNBrcb(int32_t nums, LocalTensor<float> &gammaLocal,
                                                  LocalTensor<float> &betaLocal) {
    event_t eventSV = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::S_V));
    event_t eventVS = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::V_S));

    LocalTensor<float> xLocalFp32 = xBufFp32.Get<float>();
    LocalTensor<float> yLocalFp32 = yBufFp32.Get<float>();
    LocalTensor<float> zLocalFp32 = zBufFp32.Get<float>();

    LocalTensor<float> meanLocal = meanQue.template AllocTensor<float>();
    LocalTensor<float> rstdLocal = rstdQue.template AllocTensor<float>();

    int32_t elementNum = numLastDimAligned * nums;

    // 1.1. mean process: 1/N * x_sum
    Muls(xLocalFp32, zLocalFp32, aveNum, elementNum);
    // 1.2. init buffer for reduce
    Duplicate(yLocalFp32, ZERO, nums * ELEM_PER_REP_FP32);
    pipe_barrier(PIPE_V);

    // 2.1. reducesum
    const uint32_t tailCount = numLastDim % ELEM_PER_REP_FP32;
    const uint32_t repeat = nums;  // repeat < 255 * 8 = 2040
    const uint8_t repStride = numLastDimAligned / FLOAT_BLOCK_ELEM;
    ReduceSumForSmallReduceDim(meanLocal, xLocalFp32, yLocalFp32, numLastDimAligned, numLastDim, tailCount, repeat,
                               repStride);
    pipe_barrier(PIPE_V);

    // 2.2. broadcast reducesum value
    const uint32_t broadcastDim = BROADCAST_ND_DIM_NUM;
    const uint32_t broadcastAxis = BROADCAST_ND_LAST_INDEX;
    uint32_t dstShape[broadcastDim] = {(uint32_t)nums, (uint32_t)numLastDimAligned};
    uint32_t srcShape[broadcastDim] = {(uint32_t)nums, 1};
    auto sharedTmpBuffer = yLocalFp32.ReinterpretCast<uint8_t>();
    BroadCast<float, broadcastDim, broadcastAxis>(xLocalFp32, meanLocal, dstShape, srcShape, sharedTmpBuffer);
    pipe_barrier(PIPE_V);

    // 3. rstd process: x - mean
    Sub(zLocalFp32, zLocalFp32, xLocalFp32, elementNum);
    pipe_barrier(PIPE_V);

    // 4. rstd process: (x - mean) ^ 2
    Mul(xLocalFp32, zLocalFp32, zLocalFp32, elementNum);
    pipe_barrier(PIPE_V);

    // 5. rstd process: reduce( 1 / N * (x - mean) ^ 2 )
    Muls(xLocalFp32, xLocalFp32, aveNum, elementNum);
    Duplicate(yLocalFp32, ZERO, nums * ELEM_PER_REP_FP32);
    pipe_barrier(PIPE_V);
    ReduceSumForSmallReduceDim(rstdLocal, xLocalFp32, yLocalFp32, numLastDimAligned, numLastDim, tailCount, repeat,
                               repStride);
    pipe_barrier(PIPE_V);

    // 6. rstd end: 1 / sqrt( 1 / N * reduce( (x - mean) ^ 2 ) )
    Adds(rstdLocal, rstdLocal, eps, nums);
    pipe_barrier(PIPE_V);
    Sqrt(rstdLocal, rstdLocal, nums);
    Duplicate(yLocalFp32, (float)1, nums);
    pipe_barrier(PIPE_V);
    Div(rstdLocal, yLocalFp32, rstdLocal, nums);
    pipe_barrier(PIPE_V);

    // 7. broadcast reducesum value
    BroadCast<float, broadcastDim, broadcastAxis>(xLocalFp32, rstdLocal, dstShape, srcShape, sharedTmpBuffer);
    pipe_barrier(PIPE_V);
    Mul(zLocalFp32, zLocalFp32, xLocalFp32, elementNum);
    pipe_barrier(PIPE_V);

    // 8. y = (x - mean) / rstd * beta + gamma
    LocalTensor<T> yLocal = yQue.template AllocTensor<T>();
    if constexpr (!is_same<T, float>::value) {
      Level0MulFp32Short(zLocalFp32, gammaLocal, zLocalFp32, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);
      Level0AddFp32Short(zLocalFp32, betaLocal, zLocalFp32, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);

      if constexpr (is_same<T, half>::value) {
        Cast(yLocal, zLocalFp32, RoundMode::CAST_NONE, elementNum);
      } else {
        Cast(yLocal, zLocalFp32, RoundMode::CAST_RINT, elementNum);
      }
      pipe_barrier(PIPE_V);
    } else {
      Level0MulFp32Short(yLocal, gammaLocal, zLocalFp32, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);
      Level0AddFp32Short(yLocal, betaLocal, yLocal, numLastDimAligned, nums, numLastDim);
      pipe_barrier(PIPE_V);
    }

    meanQue.EnQue(meanLocal);
    rstdQue.EnQue(rstdLocal);
    yQue.EnQue(yLocal);
  }
#endif

  __aicore__ inline void CopyOut(int32_t rowIdx, int32_t rowCount) {
    LocalTensor<T> res = yQue.template DeQue<T>();
    uint32_t gmOffset = rowIdx * rowStep * numLastDim;
    DataCopyEx(yGm[gmOffset], res, numLastDim, rowCount);
    yQue.FreeTensor(res);

#if OUTPUT_MEAN_RSTD == 1
    uint32_t gmOffsetMean = rowIdx * rowStep;
    LocalTensor<float> mean = meanQue.template DeQue<float>();
    LocalTensor<float> rstd = rstdQue.template DeQue<float>();
    DataCopyEx(meanGm[gmOffsetMean], mean, rowCount);
    DataCopyEx(rstdGm[gmOffsetMean], rstd, rowCount);
    meanQue.FreeTensor(mean);
    rstdQue.FreeTensor(rstd);
#endif
  }

 private:
  TPipe *Ppipe = nullptr;
  TQue<QuePosition::VECIN, BUFFER_NUM> x1x2Que;
  TBuf<TPosition::VECCALC> gammaBuf;
  TBuf<TPosition::VECCALC> betaBuf;
  TBuf<TPosition::VECCALC> biasBuf;
  TQue<QuePosition::VECOUT, BUFFER_NUM> yQue;  // (x1 + x2) reuse this que
                                               // #if OUTPUT_MEAN_RSTD == 1
  TQue<QuePosition::VECOUT, BUFFER_NUM> meanQue;
  TQue<QuePosition::VECOUT, BUFFER_NUM> rstdQue;
  // #endif

  TBuf<TPosition::VECCALC> xBufFp32;
  TBuf<TPosition::VECCALC> yBufFp32;
  TBuf<TPosition::VECCALC> zBufFp32;

  TBuf<TPosition::VECCALC> orBufINT16;
  TBuf<TPosition::VECCALC> transposeSrcBuf, transposeDstBuf;

  GlobalTensor<T> x1Gm, x2Gm, gammaGm, betaGm, yGm, xGm, biasGm;
  GlobalTensor<float> meanGm, rstdGm, workspaceGm;
  uint32_t numCore;
  uint32_t numFirstDim;
  uint32_t numLastDim;
  uint32_t rowStep;
  uint32_t rowWork;
  uint32_t gmOffset_;
  uint32_t rowTail_;
  uint32_t colTail;
  uint32_t colMoveCnt;
  uint32_t firstDimPerTime;
  uint32_t lastDimPerTime;
  uint32_t notLastFirstDimPerCore;
  uint32_t lFirstDimPerCore;
  float eps;
  float aveNum;
  bool lastDimPad = false;
  size_t numLastDimAligned;
  size_t numLastDimAlignedFp32;
};

#endif  // __SRC_ACME_SRC_OPS_ADD_LAYER_NORM_KERNEL_ADD_LAYER_NORM_SPECIAL_REDUCE_H_
