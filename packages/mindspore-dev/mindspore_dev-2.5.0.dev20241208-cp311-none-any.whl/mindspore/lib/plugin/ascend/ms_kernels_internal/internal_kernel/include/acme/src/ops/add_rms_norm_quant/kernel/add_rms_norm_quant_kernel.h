/**
 * Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
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

/*!
 * \file add_rms_norm_quant.h
 * \brief
 */
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_KERNEL_H_
#include "add_rms_norm_quant_base.h"

using namespace AscendC;

template <typename T>
class KernelAddRmsNormQuant {
 public:
  __aicore__ inline KernelAddRmsNormQuant(TPipe *pipe) { Ppipe = pipe; }
  __aicore__ inline void Init(GM_ADDR x1, GM_ADDR x2, GM_ADDR gamma, GM_ADDR scales1, GM_ADDR scales2,
                              GM_ADDR zero_points1, GM_ADDR zero_points2, GM_ADDR y1, GM_ADDR y2, GM_ADDR x,
                              const AddRmsNormQuantTilingData *tilingData) {
    ASSERT(GetBlockNum() != 0 && "Block dim can not be zero!");
    this->numRow = tilingData->num_row;
    this->numCol = tilingData->num_col;
    this->blockFactor = tilingData->block_factor;
    this->rowFactor = tilingData->row_factor;
    this->ubFactor = tilingData->ub_factor;
    this->epsilon = tilingData->epsilon;
    this->avgFactor = (float)1.0 / numCol;
    this->hasZeroPoints1 = tilingData->has_zeropoints1;
    this->is_broadcast = tilingData->is_broadcast;

    if (GetBlockIdx() < GetBlockNum() - 1) {
      this->rowWork = blockFactor;
    } else if (GetBlockIdx() == GetBlockNum() - 1) {
      this->rowWork = numRow - (GetBlockNum() - 1) * blockFactor;
    } else {
    }
    // get start index for current core, core parallel
    x1Gm.SetGlobalBuffer((__gm__ T *)x1 + GetBlockIdx() * blockFactor * numCol, rowWork * numCol);
    x2Gm.SetGlobalBuffer((__gm__ T *)x2 + GetBlockIdx() * blockFactor * numCol, rowWork * numCol);
    gammaGm.SetGlobalBuffer((__gm__ T *)gamma, numCol);
    scales1Gm.SetGlobalBuffer((__gm__ float *)scales1, numCol);
    if (hasZeroPoints1) {
      zeroPoints1Gm.SetGlobalBuffer((__gm__ int32_t *)zero_points1, numCol);
    }
    y1Gm.SetGlobalBuffer((__gm__ int8_t *)y1 + GetBlockIdx() * blockFactor * numCol, rowWork * numCol);
    y2Gm.SetGlobalBuffer((__gm__ int8_t *)y2 + GetBlockIdx() * blockFactor * numCol, rowWork * numCol);
    xGm.SetGlobalBuffer((__gm__ T *)x + GetBlockIdx() * blockFactor * numCol, rowWork * numCol);

    // pipe alloc memory to queue, the unit is Bytes
    Ppipe->InitBuffer(inQueueX, BUFFER_NUM, ubFactor * sizeof(T));
    Ppipe->InitBuffer(inQueueGamma, BUFFER_NUM, ubFactor * sizeof(T));
    Ppipe->InitBuffer(outQueueY1, BUFFER_NUM, ubFactor * sizeof(T));

    Ppipe->InitBuffer(scales1Buf, ubFactor * sizeof(float));
    Ppipe->InitBuffer(zeroPoints1Buf, ubFactor * sizeof(int32_t));
    if constexpr (is_same<T, half>::value || is_same<T, bfloat16_t>::value) {
      Ppipe->InitBuffer(xFp32Buf, ubFactor * sizeof(float));
    }
    Ppipe->InitBuffer(sqxBuf, ubFactor * sizeof(float));
    Ppipe->InitBuffer(reduceFp32Buf, NUM_PER_REP_FP32 * sizeof(float));
  }

  __aicore__ inline void Process() {
    CopyInGamma();
    LocalTensor<T> gammaLocal = inQueueGamma.DeQue<T>();

    uint32_t iOMax = CeilDiv(rowWork, rowFactor);
    uint32_t rowTail = rowWork - (iOMax - 1) * rowFactor;

    for (uint32_t iO = 0; iO < iOMax - 1; iO++) {
      SubProcess(iO, rowFactor, gammaLocal);
    }
    SubProcess(iOMax - 1, rowTail, gammaLocal);
    inQueueGamma.FreeTensor(gammaLocal);
  }

  __aicore__ inline void SubProcess(uint32_t iO, uint32_t calcRowNum, LocalTensor<T> &gammaLocal) {
    for (uint32_t iI = 0; iI < calcRowNum; iI++) {
      uint32_t gmBias = (iO * rowFactor + iI) * numCol;
      CopyIn(gmBias);
      Compute(iI, gammaLocal);
      CopyOutY(gmBias);
    }
  }

 private:
  __aicore__ inline void CopyIn(uint32_t gmBias) {
    LocalTensor<T> x1LocalIn = inQueueX.AllocTensor<T>();
    LocalTensor<T> x2Local = sqxBuf.Get<T>();
    LocalTensor<T> xLocal = outQueueY1.AllocTensor<T>();

    if constexpr (is_same<T, half>::value || is_same<T, bfloat16_t>::value) {
      x2Local = x2Local[ubFactor];
    }

    DataCopyCustom<T>(x1LocalIn, x1Gm[gmBias], numCol);
    DataCopyCustom<T>(x2Local, x2Gm[gmBias], numCol);
    inQueueX.EnQue(x1LocalIn);
    auto x1Local = inQueueX.DeQue<T>();

    if constexpr (is_same<T, half>::value) {
      LocalTensor<float> x1Fp32Local = xFp32Buf.Get<float>();
      Add(xLocal, x1Local, x2Local, numCol);
      pipe_barrier(PIPE_V);
      Cast(x1Fp32Local, xLocal, RoundMode::CAST_NONE, numCol);
      pipe_barrier(PIPE_V);
    } else if constexpr (is_same<T, bfloat16_t>::value) {
      LocalTensor<float> x1Fp32Local = xFp32Buf.Get<float>();
      LocalTensor<float> x2_fp32 = sqxBuf.Get<float>();
      Cast(x1Fp32Local, x1Local, RoundMode::CAST_NONE, numCol);
      Cast(x2_fp32, x2Local, RoundMode::CAST_NONE, numCol);
      pipe_barrier(PIPE_V);
      Add(x1Fp32Local, x1Fp32Local, x2_fp32, numCol);
      pipe_barrier(PIPE_V);
      Cast(xLocal, x1Fp32Local, RoundMode::CAST_RINT, numCol);
      pipe_barrier(PIPE_V);
    } else {
      Add(x1Local, x1Local, x2Local, numCol);
      pipe_barrier(PIPE_V);
      Adds(xLocal, x1Local, (float)0, numCol);
    }
    inQueueX.FreeTensor(x1Local);

    // CopyOut x1 + x2
    outQueueY1.EnQue(xLocal);
    auto xOut = outQueueY1.DeQue<T>();
    DataCopyCustom<T>(xGm[gmBias], xOut, numCol);
    outQueueY1.FreeTensor(xOut);
  }

  __aicore__ inline void CopyInGamma() {
    LocalTensor<float> scales1Local = scales1Buf.Get<float>();
    if (is_broadcast) {
      DataCopyCustom<float>(scales1Local, scales1Gm, 1);
    } else {
      DataCopyCustom<float>(scales1Local, scales1Gm, numCol);
    }
    if (hasZeroPoints1) {
      LocalTensor<int32_t> zeroPoints1Int32 = zeroPoints1Buf.Get<int32_t>();
      if (is_broadcast) {
        DataCopyCustom<int32_t>(zeroPoints1Int32, zeroPoints1Gm, 1);
        event_t event_mte2_v = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::MTE2_V));
        set_flag(PIPE_MTE2, PIPE_V, event_mte2_v);
        wait_flag(PIPE_MTE2, PIPE_V, event_mte2_v);
        Cast(zeroPoints1Int32.ReinterpretCast<float>(), zeroPoints1Int32, RoundMode::CAST_NONE, 1);
      } else {
        DataCopyCustom<int32_t>(zeroPoints1Int32, zeroPoints1Gm, numCol);
        event_t event_mte2_v = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::MTE2_V));
        set_flag(PIPE_MTE2, PIPE_V, event_mte2_v);
        wait_flag(PIPE_MTE2, PIPE_V, event_mte2_v);
        Cast(zeroPoints1Int32.ReinterpretCast<float>(), zeroPoints1Int32, RoundMode::CAST_NONE, numCol);
      }
      pipe_barrier(PIPE_V);
    }
    LocalTensor<T> gammaLocal = inQueueGamma.AllocTensor<T>();
    DataCopyCustom<T>(gammaLocal, gammaGm, numCol);
    inQueueGamma.EnQue(gammaLocal);
  }

  __aicore__ inline void Compute(uint32_t inner_progress, LocalTensor<half> gammaLocal) {
    LocalTensor<float> xFp32Local = xFp32Buf.Get<float>();
    LocalTensor<float> sqx = sqxBuf.Get<float>();
    LocalTensor<float> reduceLocal = reduceFp32Buf.Get<float>();

    Mul(sqx, xFp32Local, xFp32Local, numCol);
    pipe_barrier(PIPE_V);

    Muls(sqx, sqx, avgFactor, numCol);
    pipe_barrier(PIPE_V);

    ReduceSumCustom(sqx, sqx, reduceLocal, numCol);
    pipe_barrier(PIPE_V);

    Adds(sqx, sqx, epsilon, 1);
    pipe_barrier(PIPE_V);

    Sqrt(sqx, sqx, 1);
    Duplicate(reduceLocal, ONE, 1);
    pipe_barrier(PIPE_V);
    Div(sqx, reduceLocal, sqx, 1);
    pipe_barrier(PIPE_V);
    event_t event_v_s = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::V_S));
    set_flag(PIPE_V, PIPE_S, event_v_s);
    wait_flag(PIPE_V, PIPE_S, event_v_s);
    float rstdValue = sqx.GetValue(0);
    event_t event_s_v = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::S_V));
    set_flag(PIPE_S, PIPE_V, event_s_v);
    wait_flag(PIPE_S, PIPE_V, event_s_v);
    Muls(xFp32Local, xFp32Local, rstdValue, numCol);
    pipe_barrier(PIPE_V);

    LocalTensor<half> xFp16Cast = sqxBuf.Get<half>();
    Cast(xFp16Cast, xFp32Local, RoundMode::CAST_NONE, numCol);
    pipe_barrier(PIPE_V);
    Mul(xFp16Cast, gammaLocal, xFp16Cast, numCol);
    pipe_barrier(PIPE_V);
    Cast(xFp32Local, xFp16Cast, RoundMode::CAST_NONE, numCol);
    pipe_barrier(PIPE_V);

    event_t event_v_mte = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::V_MTE2));
    set_flag(PIPE_V, PIPE_MTE2, event_v_mte);
    wait_flag(PIPE_V, PIPE_MTE2, event_v_mte);

    LocalTensor<float> scales1Local = scales1Buf.Get<float>();
    if (is_broadcast) {
      float scaleValue = 1 / scales1Local.GetValue(0);
      set_flag(PIPE_S, PIPE_V, event_s_v);
      wait_flag(PIPE_S, PIPE_V, event_s_v);
      Muls(xFp32Local, xFp32Local, scaleValue, numCol);
    } else {
      Div(xFp32Local, xFp32Local, scales1Local, numCol);
    }
    pipe_barrier(PIPE_V);

    if (hasZeroPoints1) {
      LocalTensor<float> zeroPoints1Fp32 = zeroPoints1Buf.Get<float>();
      if (is_broadcast) {
        float offsetValue = zeroPoints1Fp32.GetValue(0);
        set_flag(PIPE_S, PIPE_V, event_s_v);
        wait_flag(PIPE_S, PIPE_V, event_s_v);
        Adds(xFp32Local, xFp32Local, offsetValue, numCol);
      } else {
        Add(xFp32Local, xFp32Local, zeroPoints1Fp32, numCol);
      }
      pipe_barrier(PIPE_V);
    }

    LocalTensor<int8_t> y1Local = outQueueY1.AllocTensor<int8_t>();
    RoundFloat2Int8(y1Local, xFp32Local, numCol);
    outQueueY1.EnQue<int8_t>(y1Local);
  }

  __aicore__ inline void CopyOutY(uint32_t progress) {
    LocalTensor<int8_t> yLocal = outQueueY1.DeQue<int8_t>();
    DataCopyCustom<int8_t>(y1Gm[progress], yLocal, numCol);
    outQueueY1.FreeTensor(yLocal);
  }

 private:
  TPipe *Ppipe = nullptr;
  // create queues for input, in this case depth is equal to buffer num
  TQue<QuePosition::VECIN, BUFFER_NUM> inQueueX, inQueueGamma;
  // create queues for output, in this case depth is equal to buffer num
  TQue<QuePosition::VECOUT, BUFFER_NUM> outQueueY1;

  TBuf<TPosition::VECCALC> scales1Buf;
  TBuf<TPosition::VECCALC> zeroPoints1Buf;
  TBuf<TPosition::VECCALC> xFp32Buf;
  TBuf<TPosition::VECCALC> sqxBuf;
  TBuf<TPosition::VECCALC> reduceFp32Buf;
  GlobalTensor<T> x1Gm;
  GlobalTensor<T> x2Gm;
  GlobalTensor<T> gammaGm;
  GlobalTensor<float> scales1Gm;
  GlobalTensor<float> scales2Gm;
  GlobalTensor<int32_t> zeroPoints1Gm;
  GlobalTensor<int32_t> zeroPoints2Gm;
  GlobalTensor<int8_t> y1Gm;
  GlobalTensor<int8_t> y2Gm;
  GlobalTensor<T> xGm;

  uint32_t numRow;
  uint32_t numCol;
  uint32_t blockFactor;  // number of calculations rows on each core
  uint32_t rowFactor;
  uint32_t ubFactor;
  float epsilon;
  float avgFactor;
  uint32_t hasZeroPoints1;
  bool is_broadcast;

  uint32_t rowWork = 1;
};
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_KERNEL_H_