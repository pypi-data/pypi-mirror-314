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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_KERNEL_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_KERNEL_UTILS_H_

namespace mindspore {
namespace acme {
namespace tiling {

#define __force_inline__ inline __attribute__((always_inline))

constexpr uint32_t L1_SIZE = 524288;
constexpr uint32_t CONST_2 = 2;
constexpr uint32_t CONST_4 = 4;
constexpr uint32_t CONST_8 = 8;
constexpr uint32_t CONST_16 = 16;
constexpr uint32_t CONST_32 = 32;
constexpr uint32_t CONST_128 = 128;
constexpr uint32_t CONST_256 = 256;

constexpr uint32_t ND2NZ_STRIDE_LIMIT = 65536;
constexpr uint32_t L0AB_PINGPONG_BUFFER_LEN_FP16 = 16384;         // 32 KB
constexpr uint32_t L0AB_PINGPONG_BUFFER_LEN_INT8 = 32768;         // 32 KB
constexpr uint32_t CUBE_MATRIX_SIZE_256 = 256;                    // 16 * 16
constexpr uint32_t CUBE_MATRIX_SIZE_512 = 512;                    // 16 * 32
constexpr uint32_t L1_PINGPONG_BUFFER_LEN_FP16 = 131072;          // 256 KB
constexpr uint32_t L1_PINGPONG_BUFFER_LEN_INT8 = 262144;          // 256 KB
constexpr uint32_t SCALE_L1_LEN = 4096;
constexpr uint32_t BIAS_L1_LEN = 2048;

constexpr uint32_t ALGO_PP = 0;
constexpr uint32_t ALGO_LLM_CUSTOM = 1;
constexpr uint32_t DTYPE_FP16 = 0;
constexpr uint32_t DTYPE_BF16 = 1;
constexpr uint32_t DTYPE_INT8 = 2;

constexpr uint32_t AIC_FINISH_FLAG_ID = 1;
constexpr uint32_t AIV_FINISH_FLAG_ID_MODE_0 = 2;
constexpr uint32_t AIV_FINISH_FLAG_ID_MODE_2 = 3;
constexpr uint32_t MAX_HW_SYNC_COUNTER = 15;
constexpr uint32_t SYNC_MODE_0 = 0;
constexpr uint32_t SYNC_MODE_1 = 1;
constexpr uint32_t SYNC_MODE_2 = 2;

enum class DataFormat { ND, NZ };

template <typename Tp, Tp v>
struct integral_constant {
  static constexpr Tp value = v;
};
using true_type = integral_constant<bool, true>;
using false_type = integral_constant<bool, false>;
template <typename, typename>
struct is_same : public false_type {};
template <typename Tp>
struct is_same<Tp, Tp> : public true_type {};

__aicore__ __force_inline__ uint64_t RoundUp(const uint64_t v, const uint64_t r) { return (v + r - 1) / r * r; }

__aicore__ __force_inline__ uint64_t CeilDiv(const uint64_t v, const uint64_t r) { return (v + r - 1) / r; }

__aicore__ __force_inline__ void GetBlockIdx(uint32_t m_loop, uint32_t n_loop, uint32_t swizzle_cnt,
                                             uint32_t swizzle_dir, uint32_t num_core, uint32_t index,
                                             uint32_t &m_idx, uint32_t &n_idx) {
  uint32_t in_batch_idx = index % (m_loop * n_loop);
  if (swizzle_dir == 0) {  // Zn
    uint32_t tile_block_loop = (m_loop + swizzle_cnt - 1) / swizzle_cnt;
    uint32_t tile_block_idx = in_batch_idx / (swizzle_cnt * n_loop);
    uint32_t in_tile_block_idx = in_batch_idx % (swizzle_cnt * n_loop);

    uint32_t n_row = swizzle_cnt;
    if (tile_block_idx == tile_block_loop - 1) {
      n_row = m_loop - swizzle_cnt * tile_block_idx;
    }
    m_idx = tile_block_idx * swizzle_cnt + in_tile_block_idx % n_row;
    n_idx = in_tile_block_idx / n_row;
    if (tile_block_idx % 2 != 0) {
      n_idx = n_loop - n_idx - 1;
    }
  } else if (swizzle_dir == 1) {  // Nz
    uint32_t tile_block_loop = (n_loop + swizzle_cnt - 1) / swizzle_cnt;
    uint32_t tile_block_idx = in_batch_idx / (swizzle_cnt * m_loop);
    uint32_t in_tile_block_idx = in_batch_idx % (swizzle_cnt * m_loop);

    uint32_t n_col = swizzle_cnt;
    if (tile_block_idx == tile_block_loop - 1) {
      n_col = n_loop - swizzle_cnt * tile_block_idx;
    }
    m_idx = in_tile_block_idx / n_col;
    n_idx = tile_block_idx * swizzle_cnt + in_tile_block_idx % n_col;
    if (tile_block_idx % 2 != 0) {
      m_idx = m_loop - m_idx - 1;
    }
  } else if (swizzle_dir == 2) { // Nn
    uint32_t n_swizzle_cnt = num_core / swizzle_cnt;
    uint32_t m_tail_swizzle_cnt = m_loop % swizzle_cnt;
    uint32_t n_tail_swizzle_cnt = n_loop % n_swizzle_cnt;
    uint32_t m_tile_block_loop = CeilDiv(m_loop, swizzle_cnt);
    uint32_t n_tile_block_loop = CeilDiv(n_loop, n_swizzle_cnt);

    // Determine the n_block of the column where the index is located.
    uint32_t n_tile_block_size = m_loop * n_swizzle_cnt;
    uint32_t n_tile_block_idx = index / n_tile_block_size;
    uint32_t n_tile_block_index = index - n_tile_block_size * n_tile_block_idx;
    uint32_t n_block_size = n_swizzle_cnt;
    if ((n_tile_block_idx == n_tile_block_loop - 1) && (n_tail_swizzle_cnt != 0)) {
      n_block_size = n_tail_swizzle_cnt;
    }

    uint32_t m_tile_block_size = swizzle_cnt * n_block_size;
    uint32_t m_tile_block_idx = n_tile_block_index / m_tile_block_size;
    uint32_t m_tile_block_index = n_tile_block_index - m_tile_block_size * m_tile_block_idx;

    uint32_t m_block_size = swizzle_cnt;
    if ((m_tile_block_idx == m_tile_block_loop - 1) && (m_tail_swizzle_cnt != 0)) {
       m_block_size = m_tail_swizzle_cnt;
    }
    uint32_t block_size = m_block_size * n_block_size;
    uint32_t in_tile_block_idx = m_tile_block_index % block_size;

    m_idx = m_tile_block_idx * swizzle_cnt + in_tile_block_idx % m_block_size;
    n_idx = n_tile_block_idx * n_swizzle_cnt + in_tile_block_idx / m_block_size;
  }
}

#ifdef __DAV_C220_CUBE__

template <typename Dtype, DataFormat srcDataFormat, DataFormat dstDataFormat>
__aicore__ __force_inline__ void CopyGmToL1(__cbuf__ Dtype *dst, __gm__ Dtype *src, uint64_t row, uint64_t col,
                                            uint64_t tile_row, uint64_t tile_col, uint32_t dstNzC0Stride) {}

template <>
__aicore__ __force_inline__ void CopyGmToL1<half, DataFormat::ND, DataFormat::NZ>(
  __cbuf__ half *dst, __gm__ half *src, uint64_t row, uint64_t col, uint64_t tile_row, uint64_t tile_col,
  uint32_t dstNzC0Stride) {
  if (col < ND2NZ_STRIDE_LIMIT) {
    copy_gm_to_cbuf_multi_nd2nz_b16(dst, src,
                                    0,                    // sid
                                    1,                    // ndNum
                                    tile_row,             // nValue
                                    tile_col,             // dValue
                                    0,                    // srcNdMatrixStride, unused
                                    col,                  // srcDValue
                                    dstNzC0Stride,        // dstNzC0Stride
                                    1,                    // dstNzNStride
                                    0                     // dstNzMatrixStride, unused
    );
  } else {
    for (uint64_t i = 0; i < tile_row; i++) {
      copy_gm_to_cbuf_multi_nd2nz_b16(dst + i * CONST_16,   // dst
                                      src + i * col,        // src
                                      0,                    // sid
                                      1,                    // ndNum
                                      1,                    // nValue
                                      tile_col,             // dValue
                                      0,                    // srcNdMatrixStride, unused
                                      0,                    // srcDValue, unused
                                      dstNzC0Stride,        // dstNzC0Stride
                                      0,                    // dstNzNStride, unused
                                      0                     // dstNzMatrixStride, unused
      );
    }
  }
}

template <>
__aicore__ __force_inline__ void CopyGmToL1<bfloat16_t, DataFormat::ND, DataFormat::NZ>(
  __cbuf__ bfloat16_t *dst, __gm__ bfloat16_t *src, uint64_t row, uint64_t col, uint64_t tile_row, uint64_t tile_col,
  uint32_t dstNzC0Stride) {
  if (col < ND2NZ_STRIDE_LIMIT) {
    copy_gm_to_cbuf_multi_nd2nz_b16(dst,                  // dst
                                    src,                  // src
                                    0,                    // sid
                                    1,                    // ndNum
                                    tile_row,             // nValue
                                    tile_col,             // dValue
                                    0,                    // srcNdMatrixStride, unused
                                    col,                  // srcDValue
                                    dstNzC0Stride,        // dstNzC0Stride
                                    1,                    // dstNzNStride
                                    0                     // dstNzMatrixStride, unused
    );
  } else {
    for (uint64_t i = 0; i < tile_row; i++) {
      copy_gm_to_cbuf_multi_nd2nz_b16(dst + i * CONST_16,   // dst
                                      src + i * col,        // src
                                      0,                    // sid
                                      1,                    // ndNum
                                      1,                    // nValue
                                      tile_col,             // dValue
                                      0,                    // srcNdMatrixStride, unused
                                      0,                    // srcDValue, unused
                                      dstNzC0Stride,        // dstNzC0Stride
                                      0,                    // dstNzNStride, unused
                                      0                     // dstNzMatrixStride, unused
      );
    }
  }
}

template <>
__aicore__ __force_inline__ void CopyGmToL1<int8_t, DataFormat::ND, DataFormat::NZ>(
  __cbuf__ int8_t *dst, __gm__ int8_t *src, uint64_t row, uint64_t col, uint64_t tile_row, uint64_t tile_col,
  uint32_t dstNzC0Stride) {
  if (col < ND2NZ_STRIDE_LIMIT) {
    copy_gm_to_cbuf_multi_nd2nz_b8(dst,                  // dst
                                   src,                  // src
                                   0,                    // sid
                                   1,                    // ndNum
                                   tile_row,             // nValue
                                   tile_col,             // dValue
                                   0,                    // srcNdMatrixStride, unused
                                   col,                  // srcDValue
                                   dstNzC0Stride,        // dstNzC0Stride
                                   1,                    // dstNzNStride
                                   0                     // dstNzMatrixStride, unused
    );
  } else {
    for (uint64_t i = 0; i < tile_row; i++) {
      copy_gm_to_cbuf_multi_nd2nz_b8(dst + i * CONST_32,   // dst
                                     src + i * col,        // src
                                     0,                    // sid
                                     1,                    // ndNum
                                     1,                    // nValue
                                     tile_col,             // dValue
                                     0,                    // srcNdMatrixStride, unused
                                     0,                    // srcDValue, unused
                                     dstNzC0Stride,        // dstNzC0Stride
                                     0,                    // dstNzNStride, unused
                                     0                     // dstNzMatrixStride, unused
      );
    }
  }
}
#elif __DAV_C220_VEC__

template<typename tensor_type>
__aicore__ __force_inline__ void CastToF32(__ubuf__ float *tensor_f32, __ubuf__ tensor_type *tensor_f16,
                                           uint64_t offset) {}

template<>
__aicore__ __force_inline__ void CastToF32<half>(__ubuf__ float *tensor_f32, __ubuf__ half *tensor_f16,
                                                 uint64_t offset) {
  vconv_f162f32(((__ubuf__ float *)tensor_f32 + offset), ((__ubuf__ half *)tensor_f16 + offset), 1, 1, 1, 8, 4);
}

template<>
__aicore__ __force_inline__ void CastToF32<bfloat16_t>(__ubuf__ float *tensor_f32, __ubuf__ bfloat16_t *tensor_f16,
                                                       uint64_t offset) {
  vconv_bf162f32(((__ubuf__ float *)tensor_f32 + offset), ((__ubuf__ bfloat16_t *)tensor_f16 + offset), 1, 1, 1, 8, 4);
}

template<typename tensor_type>
__aicore__ __force_inline__ void CastToF16(__ubuf__ float *tensor_f32, __ubuf__ tensor_type *tensor_f16,
                                           uint64_t offset) {}

template<>
__aicore__ __force_inline__ void CastToF16<half>(__ubuf__ float *tensor_f32, __ubuf__ half *tensor_f16,
                                                 uint64_t offset) {
  vconv_f322f16(((__ubuf__ half *)tensor_f16 + offset), ((__ubuf__ float *)tensor_f32 + offset), 1, 1, 1, 4, 8);
}

template<>
__aicore__ __force_inline__ void CastToF16<bfloat16_t>(__ubuf__ float *tensor_f32, __ubuf__ bfloat16_t *tensor_f16,
                                                       uint64_t offset) {
  vconv_f322bf16r(((__ubuf__ bfloat16_t *)tensor_f16 + offset), ((__ubuf__ float *)tensor_f32 + offset), 1, 1, 1, 4, 8);
}

template<typename tensor_type>
__aicore__ __force_inline__ void CopyGmToUb(__gm__ tensor_type *gm_tensor, __ubuf__ tensor_type *ub_tensor,
                                            uint64_t offset, uint16_t n_burst, uint16_t total_length,
                                            uint16_t len_burst_round, uint16_t len_burst_actucal,
                                            bool aligned) {}

template<>
__aicore__ __force_inline__ void CopyGmToUb<half>(__gm__ half *gm_tensor, __ubuf__ half *ub_tensor,
                                                  uint64_t offset, uint16_t n_burst, uint16_t total_length,
                                                  uint16_t len_burst_round, uint16_t len_burst_actucal,
                                                  bool aligned) {
  if (aligned) {
    copy_gm_to_ubuf(
        ub_tensor,
        gm_tensor + offset,
        0,                                            // sid
        n_burst,                                      // nBurst
        len_burst_round / CONST_16,                   // lenBurst
        (total_length - len_burst_round) / CONST_16,  // srcStride
        0                                             // dstStride
    );
  } else {
    copy_gm_to_ubuf_align_b16(
        ub_tensor,
        gm_tensor + offset,
        0,                                                  // sid
        n_burst,                                            // nBurst
        len_burst_actucal * sizeof(half),                   // lenBurst
        0,                                                  // leftPaddingNum
        0,                                                  // rightPaddingNum
        (total_length - len_burst_actucal) * sizeof(half),  // srcGap
        0                                                   // dstGap
    );
  }
}

template<>
__aicore__ __force_inline__ void CopyGmToUb<bfloat16_t>(__gm__ bfloat16_t *gm_tensor, __ubuf__ bfloat16_t *ub_tensor,
                                                        uint64_t offset, uint16_t n_burst, uint16_t total_length,
                                                        uint16_t len_burst_round, uint16_t len_burst_actucal,
                                                        bool aligned) {
  if (aligned) {
    copy_gm_to_ubuf(
        ub_tensor,
        gm_tensor + offset,
        0,                                              // sid
        n_burst,                                        // nBurst
        len_burst_round / CONST_16,                     // lenBurst
        (total_length - len_burst_round) / CONST_16,    // srcStride
        0                                               // dstStride
    );
  } else {
    copy_gm_to_ubuf_align_b16(
        ub_tensor,
        gm_tensor + offset,
        0,                                                         // sid
        n_burst,                                                   // nBurst
        len_burst_actucal * sizeof(bfloat16_t),                    // lenBurst
        0,                                                         // leftPaddingNum
        0,                                                         // rightPaddingNum
        (total_length - len_burst_actucal) * sizeof(bfloat16_t),   // srcGap
        0                                                          // dstGap
    );
  }
}

template<typename tensor_type>
__aicore__ __force_inline__ void CopyUbToGm(__gm__ tensor_type *gm_tensor, __ubuf__ tensor_type *ub_tensor,
                                            uint64_t offset, uint16_t n_burst, uint16_t total_length,
                                            uint16_t len_burst_round, uint16_t len_burst_actucal,
                                            bool aligned) {}

template<>
__aicore__ __force_inline__ void CopyUbToGm<half>(__gm__ half *gm_tensor, __ubuf__ half *ub_tensor,
                                                  uint64_t offset, uint16_t n_burst, uint16_t total_length,
                                                  uint16_t len_burst_round, uint16_t len_burst_actucal,
                                                  bool aligned) {
  if (aligned) {
    copy_ubuf_to_gm(
        gm_tensor + offset,
        ub_tensor,
        0,
        n_burst,                                      // nBurst
        len_burst_round / CONST_16,                   // lenBurst
        0,                                            // srcStride
        (total_length - len_burst_round) / CONST_16   // dstStride
    );
  } else {
    copy_ubuf_to_gm_align_b16(
        gm_tensor + offset,
        ub_tensor,
        0,
        n_burst,                                             // nBurst
        len_burst_actucal * sizeof(half),                    // lenBurst
        0,                                                   // leftPaddingNum
        0,                                                   // rightPaddingNum
        0,                                                   // srcGap
        (total_length - len_burst_actucal) * sizeof(half)    // dstGap
    );
  }
}

template<>
__aicore__ __force_inline__ void CopyUbToGm<bfloat16_t>(__gm__ bfloat16_t *gm_tensor, __ubuf__ bfloat16_t *ub_tensor,
                                                        uint64_t offset, uint16_t n_burst, uint16_t total_length,
                                                        uint16_t len_burst_round, uint16_t len_burst_actucal,
                                                        bool aligned) {
  if (aligned) {
    copy_ubuf_to_gm(
        gm_tensor + offset,
        ub_tensor,
        0,
        n_burst,                                      // nBurst
        len_burst_round / CONST_16,                   // lenBurst
        0,                                            // srcStride
        (total_length - len_burst_round) / CONST_16   // dstStride
    );
  } else {
    copy_ubuf_to_gm_align_b16(
        gm_tensor + offset,
        ub_tensor,
        0,
        n_burst,                                                 // nBurst
        len_burst_actucal * sizeof(bfloat16_t),                  // lenBurst
        0,                                                       // leftPaddingNum
        0,                                                       // rightPaddingNum
        0,                                                       // srcGap
        (total_length - len_burst_actucal) * sizeof(bfloat16_t)  // dstGap
    );
  }
}

template<>
__aicore__ __force_inline__ void CopyUbToGm<float>(__gm__ float *gm_tensor, __ubuf__ float *ub_tensor,
                                                   uint64_t offset, uint16_t n_burst, uint16_t total_length,
                                                   uint16_t len_burst_round, uint16_t len_burst_actucal,
                                                   bool aligned) {
  if (aligned) {
    copy_ubuf_to_gm(
        gm_tensor + offset,
        ub_tensor,
        0,
        n_burst,                                      // nBurst
        len_burst_round / CONST_8,                    // lenBurst
        0,                                            // srcStride
        (total_length - len_burst_round) / CONST_8    // dstStride
    );
  } else {
    copy_ubuf_to_gm_align_b16(
        gm_tensor + offset,
        ub_tensor,
        0,
        n_burst,                                                 // nBurst
        len_burst_actucal * sizeof(float),                       // lenBurst
        0,                                                       // leftPaddingNum
        0,                                                       // rightPaddingNum
        0,                                                       // srcGap
        (total_length - len_burst_actucal) * sizeof(float)       // dstGap
    );
  }
}

#endif

}  // tiling
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_DEVICE_SRC_MATMUL_COMMON_KERNEL_UTILS_H_