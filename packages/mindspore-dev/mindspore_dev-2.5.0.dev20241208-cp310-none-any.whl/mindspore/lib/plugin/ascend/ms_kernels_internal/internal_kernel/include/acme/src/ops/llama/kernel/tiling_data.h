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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_TILING_DATA_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_TILING_DATA_H_

#define PIPE_CAST (2)
#define BLOCK_CAST (4 * 1024)
#define ASCEND_BUF_ALIGN (1024)
#define UP_DIV(x, y) (((x) + (y) - (1)) / (y))
#define ALIGN32(size) ((((size) + 32 - 1) / 32) * 32)
#define ALIGN(size, len) ((((size) + (len)-1) / (len)) * (len))
#define ALIGN_BY_TYPE(size, size_of_type, bytes) \
  ((((size) + ((bytes) / (size_of_type)) - 1) / ((bytes) / (size_of_type))) * ((bytes) / (size_of_type)))

#define ENCODER_INPUT_IDX 0
#define ENCODER_NORM_INPUT_IDX 1
#define ENCODER_LN1_GAMMA_IDX 2
#define ENCODER_LN1_BETA_IDX 3
#define ENCODER_DENSE_CONCAT_IDX 4
#define ENCODER_DENSE_Q_IDX 5
#define ENCODER_DENSE_KV_CONCAT_IDX 6
#define ENCODER_DENSE_BIAS_IDX 7
#define ENCODER_PROJECTION_IDX 8
#define ENCODER_PROJECTION_BIAS_IDX 9
#define ENCODER_LN2_GAMMA_IDX 10
#define ENCODER_LN2_BETA_IDX 11
#define ENCODER_FFN_OUT_IDX 12
#define ENCODER_FFN_OUT_BIAS_IDX 13
#define ENCODER_FFN_PROJ_IDX 14
#define ENCODER_FFN_PROJ_BIAS_IDX 15
#define ENCODER_INPUT_IDS_IDX 16
#define ENCODER_BATCH_VALID_LENGTH_IDX 17
#define ENCODER_V_EMBEDDING_IDX 18
#define ENCODER_P_EMBEDDING_IDX 19
#define ENCODER_QUERY_EMBEDDING_IDX 20
#define ENCODER_K_CACHE_IDX 21
#define ENCODER_V_CACHE_IDX 22
#define ENCODER_POS_IDS_IDX 23
#define ENCODER_LN3_GAMMA_IDX 24
#define ENCODER_LN3_BETA_IDX 25

#define ENCODER_Q_IDX 26
#define ENCODER_MASK_IDX 27
#define ENCODER_PADDING_Q_IDX 28
#define ENCODER_PADDING_KV_IDX 29
#define ENCODER_SEQ_LEN_Q_IDX 30
#define ENCODER_SEQ_LEN_KV_IDX 31
#define ENCODER_MODE_IDX 32
#define ENCODER_EXPERT_IDS_IDX 33
#define ENCODER_TOKEN_TO_TOKEN_IDX 34

#define FREQS_COS 35
#define FREQS_SIN 36
#define ENCODER_BATCH_TO_BATCH_IDX 37
#define ENCODER_MASK_DECODE_IDX 38
#define ENCODER_BLOCK_TABLE 39
#define ENCODER_ACT_BLOCK_TABLE 40

#define ENCODER_LAST_IDX 41

#define ENCODER_OUTPUT_IDX 0
#define HEAD_OUTPUT_IDX 1
#define NORM_OUTPUT_IDX 2
#define HEAD_MAX_OUTPUT_IDX 3
#define ENCODER_OUTPUT_LAST_IDX 4
typedef struct TransformerDescT {
  int head_num_;
  int kv_head_num_;
  int hid_dim_;
  int seq_;
  int vocab_size_;
  int decoder_id_num_;
  float ln_eps_ = 0;
  int batch_size_;
  int head_size_;
  int ffn_hid_dim_;
  int kv_seq_;
  float scale_;
  bool paged_attention_;
  void *block_table_;
  int table_id_;
  int64_t page_size_;
  int page_num_;
} TransformerDescT;
typedef struct VSLDescT {
  void *act_q_seq_ = nullptr;
  void *act_kv_seq_ = nullptr;
  void *q_padding_ = nullptr;
  void *kv_padding_ = nullptr;
  void *mode_per_batch_ = nullptr;
  void *batch_to_batch_ = nullptr;
  void *token_to_token_ = nullptr;
} VSLDescT;
typedef struct TransformerParamT {
  TransformerDescT desc;
  int decoder_id_;  // set in llama impl
  int *act_q_seq_ = nullptr;
  int *act_kv_seq_ = nullptr;
  int *mode_per_batch_ = nullptr;
  int *batch_to_batch_ = nullptr;
  float eps1_;
  float eps2_;
  float eps3_;
  int token_num_;
  int token_num2_;
  int rank_id_;
  int rank_num_;
  bool incremental_mode_;
  bool is_mask_;
  bool has_bias_;
  bool has_beta_;
  bool rotary_embedding_;
  bool w_nz;
  //
  bool is_query_;
  bool is_moe_;
  bool is_last_;
  bool is_embedding_;
  void *alt_stream_ptr_;
  int weight_start_;
} TransformerParamT;

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_TILING_DATA_H_
