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
 * \file rms_norm_split_d.h
 * \brief
 */
#ifndef MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_RMS_NORM_KERNEL_RMS_NORM_SPLIT_D_H_
#define MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_RMS_NORM_KERNEL_RMS_NORM_SPLIT_D_H_
#include "rms_norm_base.h"

using namespace AscendC;

template <typename T>
class KernelRmsNormSplitD {
 public:
  __aicore__ inline KernelRmsNormSplitD() {}
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
    pipe.InitBuffer(sum_buf, row_factor * NUM_PER_BLK_FP32 * sizeof(float));
    pipe.InitBuffer(reduce_fp32_buf, NUM_PER_REP_FP32 * sizeof(float));
  }

  __aicore__ inline void Process() {
    uint32_t i_o_max = CeilDiv(row_work, row_factor);
    uint32_t row_tail = row_work - (i_o_max - 1) * row_factor;
    uint32_t j_max = CeilDiv(num_col, ub_factor);
    uint32_t col_tail = num_col - (j_max - 1) * ub_factor;
    for (uint32_t i_o = 0; i_o < i_o_max - 1; i_o++) {
      SubProcess(i_o, row_factor, j_max, col_tail);
    }
    SubProcess(i_o_max - 1, row_tail, j_max, col_tail);
  }

  __aicore__ inline void SubProcess(uint32_t i_o, uint32_t calc_row_num, uint32_t j_max, uint32_t col_tail) {
    LocalTensor<float> sumLocal = sum_buf.Get<float>();

    LocalTensor<float> rstdLocal = outQueueRstd.AllocTensor<float>();
    Duplicate(rstdLocal, (float)0.0, calc_row_num);
    pipe_barrier(PIPE_V);
    for (uint32_t j = 0; j < j_max - 1; j++) {
      ComputeFormer(i_o, calc_row_num, j, rstdLocal, sumLocal, ub_factor);
    }
    // do tail
    ComputeFormer(i_o, calc_row_num, j_max - 1, rstdLocal, sumLocal, col_tail);
    ComputeRstd(rstdLocal, calc_row_num);

    for (uint32_t j = 0; j < j_max - 1; j++) {
      ComputeLatter(i_o, calc_row_num, j, rstdLocal, ub_factor);
    }
    ComputeLatter(i_o, calc_row_num, j_max - 1, rstdLocal, col_tail);
    outQueueRstd.EnQue<float>(rstdLocal);
    CopyOutRstd(i_o, calc_row_num);
  }

 private:
  __aicore__ inline void CopyIn(uint32_t i_idx, uint32_t j_idx, uint32_t num) {
    LocalTensor<T> xLocal = inQueueX.AllocTensor<T>();
    DataCopyCustom<T>(xLocal, xGm[i_idx * num_col + j_idx * ub_factor], num);
    inQueueX.EnQue(xLocal);
  }

  __aicore__ inline void ComputeFormer(uint32_t i_o_idx, uint32_t calc_row_num, uint32_t j_idx,
                                       LocalTensor<float> &rstdLocal, LocalTensor<float> &sumLocal, uint32_t num) {
    for (uint32_t i_i = 0; i_i < calc_row_num; i_i++) {
      CopyIn(i_o_idx * row_factor + i_i, j_idx, num);
      ComputeSum(i_i, sumLocal, num);
    }
    BlockReduceSumFP32(sumLocal, sumLocal, calc_row_num * NUM_PER_BLK_FP32);
    Add(rstdLocal, rstdLocal, sumLocal, calc_row_num);
    pipe_barrier(PIPE_V);
  }

  __aicore__ inline void ComputeSum(uint32_t i_i_idx, LocalTensor<float> &sumLocal, uint32_t num) {
    LocalTensor<T> xLocal = inQueueX.DeQue<T>();
    LocalTensor<float> sqx = sqx_buf.Get<float>();
    LocalTensor<float> reduce_buf_local = reduce_fp32_buf.Get<float>();
    if constexpr (is_same<T, half>::value || is_same<T, bfloat16_t>::value) {
      LocalTensor<float> x_fp32 = x_fp32_buf.Get<float>();
      Cast(x_fp32, xLocal, RoundMode::CAST_NONE, num);
      inQueueX.FreeTensor(xLocal);
      pipe_barrier(PIPE_V);
      Mul(sqx, x_fp32, x_fp32, num);
    } else {
      Mul(sqx, xLocal, xLocal, num);
      inQueueX.FreeTensor(xLocal);
    }
    pipe_barrier(PIPE_V);
    Muls(sqx, sqx, avg_factor, num);
    pipe_barrier(PIPE_V);
    ReduceSumFP32ToBlock(sumLocal[i_i_idx * 8], sqx, reduce_buf_local, num);
  }

  __aicore__ inline void ComputeRstd(LocalTensor<float> rstdLocal, uint32_t num) {
    LocalTensor<float> reduce_buf_local = reduce_fp32_buf.Get<float>();
    Adds(rstdLocal, rstdLocal, epsilon, num);
    pipe_barrier(PIPE_V);
    Sqrt(rstdLocal, rstdLocal, num);
    Duplicate(reduce_buf_local, ONE, num);
    pipe_barrier(PIPE_V);
    Div(rstdLocal, reduce_buf_local, rstdLocal, num);
    pipe_barrier(PIPE_V);
  }

  __aicore__ inline void ComputeLatter(uint32_t i_o_idx, uint32_t calc_row_num, uint32_t j_idx,
                                       LocalTensor<float> &rstdLocal, uint32_t num) {
    CopyInGamma(j_idx, num);
    LocalTensor<T> gammaLocal = inQueueGamma.DeQue<T>();
    for (uint32_t i_i = 0; i_i < calc_row_num; i_i++) {
      CopyIn(i_o_idx * row_factor + i_i, j_idx, num);
      ComputeY(i_i, gammaLocal, rstdLocal, num);
      CopyOutY(i_o_idx * row_factor + i_i, j_idx, num);
    }
    inQueueGamma.FreeTensor(gammaLocal);
  }

  __aicore__ inline void CopyInGamma(uint32_t j_idx, uint32_t num) {
    LocalTensor<T> gammaLocal = inQueueGamma.AllocTensor<T>();
    DataCopyCustom<T>(gammaLocal, gammaGm[j_idx * ub_factor], num);
    inQueueGamma.EnQue(gammaLocal);
  }

  __aicore__ inline void ComputeY(uint32_t i_i_idx, LocalTensor<half> &gammaLocal, LocalTensor<float> &rstdLocal,
                                  uint32_t num) {
    LocalTensor<half> xLocal = inQueueX.DeQue<half>();
    LocalTensor<float> x_fp32 = x_fp32_buf.Get<float>();
    LocalTensor<float> sqx = sqx_buf.Get<float>();
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    float rstd_value = rstdLocal.GetValue(i_i_idx);
    set_flag(PIPE_S, PIPE_V, EVENT_ID0);
    wait_flag(PIPE_S, PIPE_V, EVENT_ID0);
    Cast(x_fp32, xLocal, RoundMode::CAST_NONE, num);
    inQueueX.FreeTensor(xLocal);
    pipe_barrier(PIPE_V);
    Muls(x_fp32, x_fp32, rstd_value, num);
    pipe_barrier(PIPE_V);
    LocalTensor<half> yLocal = outQueueY.AllocTensor<half>();
    Cast(yLocal, x_fp32, RoundMode::CAST_NONE, num);
    pipe_barrier(PIPE_V);
    Mul(yLocal, gammaLocal, yLocal, num);
    pipe_barrier(PIPE_V);
    outQueueY.EnQue<half>(yLocal);
  }

  __aicore__ inline void ComputeY(uint32_t i_i_idx, LocalTensor<float> &gammaLocal, LocalTensor<float> &rstdLocal,
                                  uint32_t num) {
    LocalTensor<float> xLocal = inQueueX.DeQue<float>();
    LocalTensor<float> sqx = sqx_buf.Get<float>();
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    float rstd_value = rstdLocal.GetValue(i_i_idx);
    set_flag(PIPE_S, PIPE_V, EVENT_ID0);
    wait_flag(PIPE_S, PIPE_V, EVENT_ID0);
    LocalTensor<float> yLocal = outQueueY.AllocTensor<float>();
    Muls(yLocal, xLocal, rstd_value, num);
    inQueueX.FreeTensor(xLocal);
    pipe_barrier(PIPE_V);
    Mul(yLocal, gammaLocal, yLocal, num);
    pipe_barrier(PIPE_V);
    outQueueY.EnQue<float>(yLocal);
  }

  __aicore__ inline void ComputeY(uint32_t i_i_idx, LocalTensor<bfloat16_t> &gammaLocal, LocalTensor<float> &rstdLocal,
                                  uint32_t num) {
    LocalTensor<bfloat16_t> xLocal = inQueueX.DeQue<bfloat16_t>();
    LocalTensor<float> x_fp32 = x_fp32_buf.Get<float>();
    LocalTensor<float> sqx = sqx_buf.Get<float>();
    set_flag(PIPE_V, PIPE_S, EVENT_ID0);
    wait_flag(PIPE_V, PIPE_S, EVENT_ID0);
    float rstd_value = rstdLocal.GetValue(i_i_idx);
    set_flag(PIPE_S, PIPE_V, EVENT_ID0);
    wait_flag(PIPE_S, PIPE_V, EVENT_ID0);
    Cast(x_fp32, xLocal, RoundMode::CAST_NONE, num);
    inQueueX.FreeTensor(xLocal);
    pipe_barrier(PIPE_V);
    Muls(x_fp32, x_fp32, rstd_value, num);
    pipe_barrier(PIPE_V);
    LocalTensor<bfloat16_t> yLocal = outQueueY.AllocTensor<bfloat16_t>();
    Cast(yLocal, x_fp32, RoundMode::CAST_RINT, num);
    pipe_barrier(PIPE_V);
    Cast(x_fp32, yLocal, RoundMode::CAST_NONE, num);
    pipe_barrier(PIPE_V);
    Cast(sqx, gammaLocal, RoundMode::CAST_NONE, num);
    pipe_barrier(PIPE_V);
    Mul(x_fp32, x_fp32, sqx, num);
    pipe_barrier(PIPE_V);
    Cast(yLocal, x_fp32, RoundMode::CAST_RINT, num);
    pipe_barrier(PIPE_V);
    outQueueY.EnQue<bfloat16_t>(yLocal);
  }

  __aicore__ inline void CopyOutY(uint32_t i_idx, uint32_t j_idx, uint32_t num) {
    LocalTensor<T> yLocal = outQueueY.DeQue<T>();
    DataCopyCustom<T>(yGm[i_idx * num_col + j_idx * ub_factor], yLocal, num);
    outQueueY.FreeTensor(yLocal);
  }

  __aicore__ inline void CopyOutRstd(uint32_t i_o_idx, uint32_t num) {
    LocalTensor<float> rstdLocal = outQueueRstd.DeQue<float>();
#if __CCE_AICORE__ == 220
    DataCopyCustom<float>(rstdGm[i_o_idx * row_factor], rstdLocal, num);
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
  TBuf<TPosition::VECCALC> sum_buf;
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

  int tempbuf_num;
};
#endif  // MS_KERNELS_INTERNAL_SRC_ACME_SRC_OPS_RMS_NORM_KERNEL_RMS_NORM_SPLIT_D_H_