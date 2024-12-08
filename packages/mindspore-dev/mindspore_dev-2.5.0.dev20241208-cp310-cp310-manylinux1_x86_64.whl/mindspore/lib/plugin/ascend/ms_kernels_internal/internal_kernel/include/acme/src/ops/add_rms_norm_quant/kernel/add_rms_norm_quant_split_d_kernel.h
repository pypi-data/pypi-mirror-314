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
 * \file add_rms_norm_quant_split_d.h
 * \brief
 */
#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_SPLIT_D_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_SPLIT_D_KERNEL_H_
#include "add_rms_norm_quant_base.h"

using namespace AscendC;

template <typename T>
class KernelAddRmsNormQuantSplitD {
 public:
  __aicore__ inline KernelAddRmsNormQuantSplitD(TPipe *pipe) { Ppipe = pipe; }
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

    // pipe alloc memory to queue, the unit is Bytes.
    // We need 2 buffers here for both x1 and x2.
    Ppipe->InitBuffer(inQueueX, BUFFER_NUM, 2 * ubFactor * sizeof(T));
    Ppipe->InitBuffer(inQueueGamma, BUFFER_NUM, ubFactor * sizeof(T));
    Ppipe->InitBuffer(outQueueY1, BUFFER_NUM, ubFactor * sizeof(T));

    Ppipe->InitBuffer(scales1Buf, ubFactor * sizeof(float));
    Ppipe->InitBuffer(zeroPoints1Buf, ubFactor * sizeof(int32_t));
    if constexpr (is_same<T, half>::value || is_same<T, bfloat16_t>::value) {
      Ppipe->InitBuffer(xFp32Buf, ubFactor * sizeof(float));
    }
    Ppipe->InitBuffer(sqxBuf, ubFactor * sizeof(float));
    Ppipe->InitBuffer(sumBuf, rowFactor * NUM_PER_BLK_FP32 * sizeof(float));
    Ppipe->InitBuffer(reduceFp32Buf, NUM_PER_REP_FP32 * sizeof(float));
    Ppipe->InitBuffer(rstdBuf, rowFactor * sizeof(float));
  }

  __aicore__ inline void Process() {
    uint32_t iOMax = CeilDiv(rowWork, rowFactor);
    uint32_t rowTail = rowWork - (iOMax - 1) * rowFactor;
    uint32_t jMax = CeilDiv(numCol, ubFactor);
    uint32_t colTail = numCol - (jMax - 1) * ubFactor;
    for (uint32_t iO = 0; iO < iOMax - 1; iO++) {
      SubProcess(iO, rowFactor, jMax, colTail);
    }
    SubProcess(iOMax - 1, rowTail, jMax, colTail);
  }

  __aicore__ inline void SubProcess(uint32_t iO, uint32_t calcRowNum, uint32_t jMax, uint32_t colTail) {
    LocalTensor<float> sumLocal = sumBuf.Get<float>();

    LocalTensor<float> rstdLocal = rstdBuf.Get<float>();
    Duplicate(rstdLocal, (float)0.0, calcRowNum);
    pipe_barrier(PIPE_V);
    for (uint32_t j = 0; j < jMax - 1; j++) {
      ComputeFormer(iO, calcRowNum, j, rstdLocal, sumLocal, ubFactor);
    }
    // do tail
    ComputeFormer(iO, calcRowNum, jMax - 1, rstdLocal, sumLocal, colTail);
    ComputeRstd(rstdLocal, calcRowNum);

    for (uint32_t j = 0; j < jMax - 1; j++) {
      ComputeLatter(iO, calcRowNum, j, rstdLocal, ubFactor);
    }
    ComputeLatter(iO, calcRowNum, jMax - 1, rstdLocal, colTail);
  }

 private:
  __aicore__ inline void CopyInAndAdd(uint32_t iIdx, uint32_t jIdx, uint32_t num) {
    LocalTensor<T> x1x2In = inQueueX.AllocTensor<T>();
    LocalTensor<T> x1In = x1x2In[0];
    LocalTensor<T> x2In = x1x2In[ubFactor];
    DataCopyCustom<T>(x1In, x1Gm[iIdx * numCol + jIdx * ubFactor], num);
    DataCopyCustom<T>(x2In, x2Gm[iIdx * numCol + jIdx * ubFactor], num);
    inQueueX.EnQue(x1x2In);
    LocalTensor<T> x1x2Local = inQueueX.DeQue<T>();

    auto x1Local = x1x2Local[0];
    auto x2Local = x1x2Local[ubFactor];

    LocalTensor<T> xLocal = outQueueY1.AllocTensor<T>();

    if constexpr (is_same<T, half>::value) {
      LocalTensor<float> x1Fp32Local = xFp32Buf.Get<float>();

      Add(xLocal, x1Local, x2Local, num);
      pipe_barrier(PIPE_V);
      Cast(x1Fp32Local, xLocal, RoundMode::CAST_NONE, num);
      pipe_barrier(PIPE_V);
      // x1+x2 saved in x1Fp32Local
    } else if constexpr (is_same<T, bfloat16_t>::value) {
      LocalTensor<float> x1Fp32Local = xFp32Buf.Get<float>();
      LocalTensor<float> x2Fp32Local = x1x2Local.template ReinterpretCast<float>();

      Cast(x1Fp32Local, x1Local, RoundMode::CAST_NONE, num);
      pipe_barrier(PIPE_V);
      Cast(x2Fp32Local, x2Local, RoundMode::CAST_NONE, num);
      pipe_barrier(PIPE_V);

      Add(x1Fp32Local, x1Fp32Local, x2Fp32Local, num);
      pipe_barrier(PIPE_V);
      Cast(xLocal, x1Fp32Local, RoundMode::CAST_RINT, num);
      pipe_barrier(PIPE_V);
      // x1+x2 saved in x1Fp32Local
    } else {
      Add(x1Local, x1Local, x2Local, num);
      pipe_barrier(PIPE_V);
      Adds(xLocal, x1Local, (float)0.0, num);
      // x1+x2 saved in inQueueX
    }
    inQueueX.FreeTensor(x1x2Local);

    // copy out to workspace && x_out
    outQueueY1.EnQue(xLocal);
    auto x_out = outQueueY1.DeQue<T>();
    DataCopyCustom<T>(xGm[iIdx * numCol + jIdx * ubFactor], x_out, num);
    outQueueY1.FreeTensor(x_out);
  }

  __aicore__ inline void ComputeFormer(uint32_t iOIdx, uint32_t calcRowNum, uint32_t jIdx,
                                       LocalTensor<float> &rstdLocal, LocalTensor<float> &sumLocal, uint32_t num) {
    for (uint32_t i_i = 0; i_i < calcRowNum; i_i++) {
      CopyInAndAdd(iOIdx * rowFactor + i_i, jIdx, num);
      ComputeSum(i_i, sumLocal, num);
    }
    BlockReduceSumFP32(sumLocal, sumLocal, calcRowNum * NUM_PER_BLK_FP32);
    Add(rstdLocal, rstdLocal, sumLocal, calcRowNum);
    pipe_barrier(PIPE_V);
  }

  __aicore__ inline void ComputeSum(uint32_t iIIdx, LocalTensor<float> &sumLocal, uint32_t num) {
    LocalTensor<float> sqx = sqxBuf.Get<float>();
    LocalTensor<float> reduce_buf_local = reduceFp32Buf.Get<float>();
    if constexpr (is_same<T, half>::value || is_same<T, bfloat16_t>::value) {
      LocalTensor<float> xFp32Local = xFp32Buf.Get<float>();
      pipe_barrier(PIPE_V);
      Mul(sqx, xFp32Local, xFp32Local, num);
    } else {
      LocalTensor<T> xLocal = inQueueX.AllocTensor<float>();
      pipe_barrier(PIPE_V);
      Mul(sqx, xLocal, xLocal, num);
      inQueueX.FreeTensor(xLocal);
    }
    pipe_barrier(PIPE_V);
    Muls(sqx, sqx, avgFactor, num);
    pipe_barrier(PIPE_V);
    // 8 means 8 fp32 pre block
    ReduceSumFP32ToBlock(sumLocal[iIIdx * 8], sqx, reduce_buf_local, num);
  }

  __aicore__ inline void ComputeRstd(LocalTensor<float> rstdLocal, uint32_t num) {
    LocalTensor<float> reduce_buf_local = reduceFp32Buf.Get<float>();
    Adds(rstdLocal, rstdLocal, epsilon, num);
    pipe_barrier(PIPE_V);
    Sqrt(rstdLocal, rstdLocal, num);
    Duplicate(reduce_buf_local, ONE, num);
    pipe_barrier(PIPE_V);
    Div(rstdLocal, reduce_buf_local, rstdLocal, num);
    pipe_barrier(PIPE_V);
  }

  __aicore__ inline void ComputeLatter(uint32_t iOIdx, uint32_t calcRowNum, uint32_t jIdx,
                                       LocalTensor<float> &rstdLocal, uint32_t num) {
    CopyInGamma(jIdx, num);
    LocalTensor<T> gammaLocal = inQueueGamma.DeQue<T>();
    for (uint32_t i_i = 0; i_i < calcRowNum; i_i++) {
      CopyInAndAdd(iOIdx * rowFactor + i_i, jIdx, num);
      ComputeY(i_i, gammaLocal, rstdLocal, num);
      CopyOutY(iOIdx * rowFactor + i_i, jIdx, num);
    }
    inQueueGamma.FreeTensor(gammaLocal);
  }

  __aicore__ inline void CopyInGamma(uint32_t jIdx, uint32_t num) {
    LocalTensor<float> scales1Local = scales1Buf.Get<float>();
    if (is_broadcast) {
      DataCopyCustom<float>(scales1Local, scales1Gm, 1);
    } else {
      DataCopyCustom<float>(scales1Local, scales1Gm[jIdx * ubFactor], num);
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
        DataCopyCustom<int32_t>(zeroPoints1Int32, zeroPoints1Gm[jIdx * ubFactor], num);
        event_t event_mte2_v = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::MTE2_V));
        set_flag(PIPE_MTE2, PIPE_V, event_mte2_v);
        wait_flag(PIPE_MTE2, PIPE_V, event_mte2_v);
        Cast(zeroPoints1Int32.ReinterpretCast<float>(), zeroPoints1Int32, RoundMode::CAST_NONE, num);
      }
      pipe_barrier(PIPE_V);
    }
    LocalTensor<T> gammaLocal = inQueueGamma.AllocTensor<T>();
    DataCopyCustom<T>(gammaLocal, gammaGm[jIdx * ubFactor], num);
    inQueueGamma.EnQue(gammaLocal);
  }

  __aicore__ inline void ComputeY(uint32_t iIIdx, LocalTensor<half> &gammaLocal, LocalTensor<float> &rstdLocal,
                                  uint32_t num) {
    LocalTensor<float> xFp32Local = xFp32Buf.Get<float>();
    LocalTensor<float> sqx = sqxBuf.Get<float>();
    event_t event_v_s = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::V_S));
    set_flag(PIPE_V, PIPE_S, event_v_s);
    wait_flag(PIPE_V, PIPE_S, event_v_s);
    float rstdValue = rstdLocal.GetValue(iIIdx);
    event_t event_s_v = static_cast<event_t>(GetTPipePtr()->FetchEventID(HardEvent::S_V));
    set_flag(PIPE_S, PIPE_V, event_s_v);
    wait_flag(PIPE_S, PIPE_V, event_s_v);
    pipe_barrier(PIPE_V);
    Muls(xFp32Local, xFp32Local, rstdValue, num);
    pipe_barrier(PIPE_V);

    LocalTensor<half> xFp16Cast = sqxBuf.Get<half>();
    Cast(xFp16Cast, xFp32Local, RoundMode::CAST_NONE, num);
    pipe_barrier(PIPE_V);
    Mul(xFp16Cast, gammaLocal, xFp16Cast, num);
    pipe_barrier(PIPE_V);
    Cast(xFp32Local, xFp16Cast, RoundMode::CAST_NONE, num);
    pipe_barrier(PIPE_V);

    LocalTensor<float> scales1Local = scales1Buf.Get<float>();
    if (is_broadcast) {
      float scaleValue = 1 / scales1Local.GetValue(0);
      set_flag(PIPE_S, PIPE_V, event_s_v);
      wait_flag(PIPE_S, PIPE_V, event_s_v);
      Muls(xFp32Local, xFp32Local, scaleValue, num);
    } else {
      Div(xFp32Local, xFp32Local, scales1Local, num);
    }
    pipe_barrier(PIPE_V);

    if (hasZeroPoints1) {
      LocalTensor<float> zeroPoints1Fp32 = zeroPoints1Buf.Get<float>();
      if (is_broadcast) {
        float offsetValue = zeroPoints1Fp32.GetValue(0);
        set_flag(PIPE_S, PIPE_V, event_s_v);
        wait_flag(PIPE_S, PIPE_V, event_s_v);
        Adds(xFp32Local, xFp32Local, offsetValue, num);
      } else {
        Add(xFp32Local, xFp32Local, zeroPoints1Fp32, num);
      }
      pipe_barrier(PIPE_V);
    }

    LocalTensor<int8_t> y1Local = outQueueY1.AllocTensor<int8_t>();
    RoundFloat2Int8(y1Local, xFp32Local, num);
    outQueueY1.EnQue<int8_t>(y1Local);
  }

  __aicore__ inline void CopyOutY(uint32_t iIdx, uint32_t jIdx, uint32_t num) {
    LocalTensor<int8_t> yLocal = outQueueY1.DeQue<int8_t>();
    pipe_barrier(PIPE_ALL);
    DataCopyCustom<int8_t>(y1Gm[iIdx * numCol + jIdx * ubFactor], yLocal, num);
    pipe_barrier(PIPE_ALL);
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
  TBuf<TPosition::VECCALC> sumBuf;
  TBuf<TPosition::VECCALC> reduceFp32Buf;
  TBuf<TPosition::VECCALC> rstdBuf;

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

  uint32_t rowWork = 1;
  bool is_broadcast;

  int tempbufNum;
};
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_ADD_RMS_NORM_QUANT_KERNEL_ADD_RMS_NORM_QUANT_SPLIT_D_KERNEL_H_