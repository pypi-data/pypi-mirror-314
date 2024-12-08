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

/*!
 * \file rms_norm.h
 * \brief
 */
#ifndef MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_RMS_NORM_KERNEL_RMS_NORM_NORMAL_H_
#define MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_RMS_NORM_KERNEL_RMS_NORM_NORMAL_H_
#include "rms_norm_base.h"

using namespace AscendC;

template <typename T>
class KernelRmsNorm {
 public:
  __aicore__ inline KernelRmsNorm() {}
  __aicore__ inline void Init(GM_ADDR x, GM_ADDR gamma, GM_ADDR y, GM_ADDR rstd, uint32_t num_row_, uint32_t num_col_,
                              uint32_t block_factor_, uint32_t row_factor_, uint32_t ub_factor_, float epsilon_,
                              float avg_factor_) {
    ASSERT(GetBlockNum() != 0 && "block dim can not be zero!");
    this->num_row = num_row_;
    this->num_col = num_col_;
    this->block_factor = block_factor_;
    this->row_factor = row_factor_;
    this->ub_factor = ub_factor_;
    this->epsilon = epsilon_;
    this->avg_factor = (float)1.0 / num_col;

    if (GetBlockIdx() < GetBlockNum() - 1) {
      this->row_work = block_factor;
    } else if (GetBlockIdx() == GetBlockNum() - 1) {
      this->row_work = num_row - (GetBlockNum() - 1) * block_factor;
    } else {
    }
    // get start index for current core, core parallel
    xGm.SetGlobalBuffer((__gm__ T *)x + GetBlockIdx() * block_factor * num_col, row_work * num_col);
    gammaGm.SetGlobalBuffer((__gm__ T *)gamma, num_col);
    yGm.SetGlobalBuffer((__gm__ T *)y + GetBlockIdx() * block_factor * num_col, row_work * num_col);
    rstdGm.SetGlobalBuffer((__gm__ float *)rstd + GetBlockIdx() * block_factor, block_factor);

    // pipe alloc memory to queue, the unit is Bytes
    pipe.InitBuffer(inQueueX, BUFFER_NUM, ub_factor * sizeof(T));
    pipe.InitBuffer(inQueueGamma, BUFFER_NUM, ub_factor * sizeof(T));
    pipe.InitBuffer(outQueueY, BUFFER_NUM, ub_factor * sizeof(T));
    pipe.InitBuffer(outQueueRstd, BUFFER_NUM, row_factor * sizeof(float));

    if constexpr (is_same<T, half>::value || is_same<T, bfloat16_t>::value) {
      pipe.InitBuffer(x_fp32_buf, ub_factor * sizeof(float));
    }
    pipe.InitBuffer(sqx_buf, ub_factor * sizeof(float));
    pipe.InitBuffer(reduce_fp32_buf, NUM_PER_REP_FP32 * sizeof(float));
  }

  __aicore__ inline void Process() {
    CopyInGamma();
    LocalTensor<T> gammaLocal = inQueueGamma.DeQue<T>();

    uint32_t i_o_max = CeilDiv(row_work, row_factor);
    uint32_t row_tail = row_work - (i_o_max - 1) * row_factor;

    for (uint32_t i_o = 0; i_o < i_o_max - 1; i_o++) {
      SubProcess(i_o, row_factor, gammaLocal);
    }
    SubProcess(i_o_max - 1, row_tail, gammaLocal);
    inQueueGamma.FreeTensor(gammaLocal);
  }

  __aicore__ inline void SubProcess(uint32_t i_o, uint32_t calc_row_num, LocalTensor<T> &gammaLocal) {
    LocalTensor<float> rstdLocal = outQueueRstd.AllocTensor<float>();
    for (uint32_t i_i = 0; i_i < calc_row_num; i_i++) {
      uint32_t gm_bias = (i_o * row_factor + i_i) * num_col;
      CopyIn(gm_bias);
      Compute(i_i, gammaLocal, rstdLocal);
      CopyOutY(gm_bias);
    }
    outQueueRstd.EnQue<float>(rstdLocal);
    CopyOutRstd(i_o, calc_row_num);
  }

 private:
  __aicore__ inline void CopyIn(uint32_t gm_bias) {
    LocalTensor<T> xLocal = inQueueX.AllocTensor<T>();
    DataCopyCustom<T>(xLocal, xGm[gm_bias], num_col);
    inQueueX.EnQue(xLocal);
  }

  __aicore__ inline void CopyInGamma() {
    LocalTensor<T> gammaLocal = inQueueGamma.AllocTensor<T>();
    DataCopyCustom<T>(gammaLocal, gammaGm, num_col);
    inQueueGamma.EnQue(gammaLocal);
  }

  __aicore__ inline void Compute(uint32_t inner_progress, LocalTensor<half> gammaLocal, LocalTensor<float> rstdLocal) {
    LocalTensor<half> xLocal = inQueueX.DeQue<half>();
    LocalTensor<float> x_fp32 = x_fp32_buf.Get<float>();
    LocalTensor<float> sqx = sqx_buf.Get<float>();
    LocalTensor<float> reduce_buf_local = reduce_fp32_buf.Get<float>();

    Cast(x_fp32, xLocal, RoundMode::CAST_NONE, num_col);
    inQueueX.FreeTensor(xLocal);
    pipe_barrier(PIPE_V);

    Mul(sqx, x_fp32, x_fp32, num_col);
    pipe_barrier(PIPE_V);

    Muls(sqx, sqx, avg_factor, num_col);
    pipe_barrier(PIPE_V);

    ReduceSumCustom(sqx, sqx, reduce_buf_local, num_col);
    pipe_barrier(PIPE_V);

    Adds(sqx, sqx, epsilon, 1);
    pipe_barrier(PIPE_V);

    Sqrt(sqx, sqx, 1);
    Duplicate(reduce_buf_local, ONE, 1);
    pipe_barrier(PIPE_V);
    Div(sqx, reduce_buf_local, sqx, 1);
    pipe_barrier(PIPE_V);
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    float rstd_value = sqx.GetValue(0);
    set_flag(PIPE_S, PIPE_V, EVENT_ID0);
    wait_flag(PIPE_S, PIPE_V, EVENT_ID0);
    rstdLocal.SetValue(inner_progress, rstd_value);
    pipe_barrier(PIPE_V);
    Muls(x_fp32, x_fp32, rstd_value, num_col);
    pipe_barrier(PIPE_V);
    LocalTensor<half> yLocal = outQueueY.AllocTensor<half>();
    Cast(yLocal, x_fp32, RoundMode::CAST_NONE, num_col);
    pipe_barrier(PIPE_V);
    Mul(yLocal, gammaLocal, yLocal, num_col);
    pipe_barrier(PIPE_V);
    outQueueY.EnQue<half>(yLocal);
  }

  __aicore__ inline void Compute(uint32_t inner_progress, LocalTensor<float> gammaLocal, LocalTensor<float> rstdLocal) {
    LocalTensor<float> xLocal = inQueueX.DeQue<float>();
    LocalTensor<float> sqx = sqx_buf.Get<float>();
    LocalTensor<float> reduce_buf_local = reduce_fp32_buf.Get<float>();
    Mul(sqx, xLocal, xLocal, num_col);
    pipe_barrier(PIPE_V);

    Muls(sqx, sqx, avg_factor, num_col);
    pipe_barrier(PIPE_V);

    ReduceSumCustom(sqx, sqx, reduce_buf_local, num_col);
    pipe_barrier(PIPE_V);
    Adds(sqx, sqx, epsilon, 1);
    pipe_barrier(PIPE_V);

    Sqrt(sqx, sqx, 1);
    Duplicate(reduce_buf_local, ONE, 1);
    pipe_barrier(PIPE_V);
    Div(sqx, reduce_buf_local, sqx, 1);
    pipe_barrier(PIPE_V);
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    float rstd_value = sqx.GetValue(0);
    set_flag(PIPE_S, PIPE_V, EVENT_ID0);
    wait_flag(PIPE_S, PIPE_V, EVENT_ID0);
    rstdLocal.SetValue(inner_progress, rstd_value);
    pipe_barrier(PIPE_V);
    LocalTensor<float> yLocal = outQueueY.AllocTensor<float>();
    Muls(yLocal, xLocal, rstd_value, num_col);
    inQueueX.FreeTensor(xLocal);
    pipe_barrier(PIPE_V);
    Mul(yLocal, gammaLocal, yLocal, num_col);
    pipe_barrier(PIPE_V);
    outQueueY.EnQue<float>(yLocal);
  }

  __aicore__ inline void Compute(uint32_t inner_progress, LocalTensor<bfloat16_t> gammaLocal,
                                 LocalTensor<float> rstdLocal) {
    LocalTensor<bfloat16_t> xLocal = inQueueX.DeQue<bfloat16_t>();
    LocalTensor<float> x_fp32 = x_fp32_buf.Get<float>();
    LocalTensor<float> sqx = sqx_buf.Get<float>();
    LocalTensor<float> reduce_buf_local = reduce_fp32_buf.Get<float>();

    Cast(x_fp32, xLocal, RoundMode::CAST_NONE, num_col);
    inQueueX.FreeTensor(xLocal);
    pipe_barrier(PIPE_V);

    Mul(sqx, x_fp32, x_fp32, num_col);
    pipe_barrier(PIPE_V);

    Muls(sqx, sqx, avg_factor, num_col);
    pipe_barrier(PIPE_V);
    ReduceSumCustom(sqx, sqx, reduce_buf_local, num_col);
    pipe_barrier(PIPE_V);

    Adds(sqx, sqx, epsilon, 1);
    pipe_barrier(PIPE_V);

    Sqrt(sqx, sqx, 1);
    Duplicate(reduce_buf_local, ONE, 1);
    pipe_barrier(PIPE_V);
    Div(sqx, reduce_buf_local, sqx, 1);
    pipe_barrier(PIPE_V);
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    float rstd_value = sqx.GetValue(0);
    set_flag(PIPE_S, PIPE_V, EVENT_ID0);
    wait_flag(PIPE_S, PIPE_V, EVENT_ID0);
    rstdLocal.SetValue(inner_progress, rstd_value);
    pipe_barrier(PIPE_V);
    Muls(x_fp32, x_fp32, rstd_value, num_col);
    pipe_barrier(PIPE_V);
    LocalTensor<bfloat16_t> yLocal = outQueueY.AllocTensor<bfloat16_t>();
    Cast(yLocal, x_fp32, RoundMode::CAST_RINT, num_col);
    pipe_barrier(PIPE_V);
    Cast(x_fp32, yLocal, RoundMode::CAST_NONE, num_col);
    pipe_barrier(PIPE_V);
    Cast(sqx, gammaLocal, RoundMode::CAST_NONE, num_col);  // gamma_fp32 reuse sqx
    pipe_barrier(PIPE_V);
    Mul(x_fp32, x_fp32, sqx, num_col);
    pipe_barrier(PIPE_V);
    Cast(yLocal, x_fp32, RoundMode::CAST_RINT, num_col);
    pipe_barrier(PIPE_V);
    outQueueY.EnQue<bfloat16_t>(yLocal);
  }

  __aicore__ inline void CopyOutY(uint32_t progress) {
    LocalTensor<T> yLocal = outQueueY.DeQue<T>();
    DataCopyCustom<T>(yGm[progress], yLocal, num_col);
    outQueueY.FreeTensor(yLocal);
  }

  __aicore__ inline void CopyOutRstd(uint32_t outer_progress, uint32_t num) {
    LocalTensor<float> rstdLocal = outQueueRstd.DeQue<float>();
#if __CCE_AICORE__ == 220
    DataCopyCustom<float>(rstdGm[outer_progress * row_factor], rstdLocal, num);
#endif
    outQueueRstd.FreeTensor(rstdLocal);
  }

 private:
  TPipe pipe;
  // create queues for input, in this case depth is equal to buffer num
  TQue<QuePosition::VECIN, BUFFER_NUM> inQueueX, inQueueGamma;
  // create queues for output, in this case depth is equal to buffer num
  TQue<QuePosition::VECOUT, BUFFER_NUM> outQueueY, outQueueRstd;

  TBuf<TPosition::VECCALC> x_fp32_buf;
  TBuf<TPosition::VECCALC> sqx_buf;
  TBuf<TPosition::VECCALC> reduce_fp32_buf;
  GlobalTensor<T> xGm;
  GlobalTensor<T> gammaGm;
  GlobalTensor<T> yGm;
  GlobalTensor<float> rstdGm;

  uint32_t num_row;
  uint32_t num_col;
  uint32_t block_factor;  // number of calculations rows on each core
  uint32_t row_factor;
  uint32_t ub_factor;
  float epsilon;
  float avg_factor;

  uint32_t row_work = 1;
};
#endif  // MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_RMS_NORM_KERNEL_RMS_NORM_NORMAL_H_