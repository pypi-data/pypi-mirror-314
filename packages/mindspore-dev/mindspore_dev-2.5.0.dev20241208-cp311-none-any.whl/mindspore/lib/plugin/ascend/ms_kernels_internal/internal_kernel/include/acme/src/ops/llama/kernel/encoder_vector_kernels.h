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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_ENCODER_VECTOR_KERNELS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_ENCODER_VECTOR_KERNELS_H_
#define BLOCK_SIZE 11 * 1024
extern "C" void SqueezeAscendc(void *src, void *dst, VSLDescT vsl_desc, uint32_t total_token, TransformerDescT desc_d,
                               int core_num, void *stream);
extern "C" void QKVPermuteAscendc(void *qkv_ptr, void *bias_ptr, void *q_ptr, void *k_cache_ptr, void *v_cache_ptr,
                                  VSLDescT vsl_desc, void *k_prompt, void *v_prompt, void *sin, void *cos,
                                  void *block_table, int actual_token, TransformerDescT desc_d, int core_num,
                                  void *stream);
extern "C" void LayerNormAscendc(void *inputX_gm, void *inputY_gm, void *bias_gm, void *gamm_gm, void *beta_gm,
                                 void *output_gm, void *output_norm_gm, void *input_ids_gm, void *input_pos_gm,
                                 void *emmbeding_word_gm, void *emmbeding_pos_gm, uint32_t totalToken,
                                 TransformerDescT desc_d, VSLDescT vsl_desc, int core_num, void *stream);
extern "C" void KernelAddAscendc(void *in1, void *in2, void *out, int len, int vec_core_num, void *stream);
extern "C" void VocabEmbeddingAscendc(void *position_idx, void *embedding_table, void *out, VSLDescT vsl_desc,
                                      uint32_t tot_token, TransformerDescT desc_d, int core_num, void *stream);
extern "C" void CreateVSLAscendc(void *batch_valid_len_gm, void *position_idx_gm, void *q_seq_len_gm,
                                 void *kv_seq_len_gm, void *q_padding_offset_gm, void *kv_padding_offset_gm, void *mode,
                                 void *token_num_gm, void *token_to_token_gm, uint32_t batch_size, uint32_t max_seq_len,
                                 void *stream);
extern "C" void GatherHeadAscendc(void *src_gm, void *dst_gm, uint32_t total_token, TransformerDescT desc_d,
                                  VSLDescT vsl_desc, int core_num, void *stream);
extern "C" void KernelAddScatterAscendc(void *in1, void *in2, void *out, int token_num, int hidden_size,
                                        void *token_to_token_gm, int core_num, void *stream);
extern "C" void KernelCreateMoeParamAscendc(void *expert_ids, void *expert_count_by_batch, void *expert_count,
                                            void *token_to_token, void *seq_lens, void *padding_offset, void *mode,
                                            uint32_t expert_num, uint32_t moe_num, uint32_t batch_size,
                                            uint32_t seq_len, uint32_t total_token, uint32_t moe_id, float capacity,
                                            bool is_query, int core_num, void *stream);
extern "C" void KernelCreateCountExpertAscendc(void *expert_ids, void *out, void *seq_lens, void *padding_offset,
                                               void *mode, uint32_t moe_num, uint32_t expert_num, float capacity,
                                               uint32_t batch_size, uint32_t seq_len, uint32_t moe_id, bool is_query,
                                               int core_num, void *stream);
extern "C" void RMSNormAscendc(void *inputX_gm, void *inputY_gm, void *gamm_gm, void *output_gm, void *output_norm_gm,
                               void *input_ids_gm, void *emmbeding_word_gm, uint32_t tot_token, TransformerDescT desc_d,
                               VSLDescT vsl_desc, int core_num, void *stream);
extern "C" void KernelSiluAndMulAscendc(void *input_gm, void *output_gm, uint32_t total_token, uint32_t h_length,
                                        int core_num, void *stream);
extern "C" void NormalizationDistAttnAscendc(void *src, void *dst, void *softmax_max, void *softmax_sum,
                                             void *softmax_max_out, void *softmax_sum_out, VSLDescT vsl_desc,
                                             uint32_t total_token, TransformerDescT desc_p, uint32_t dist_size,
                                             int core_num, void *stream);
extern "C" void KernelCastAscendC(void *src, void *dst, uint32_t elem_num, bool f_2_h, int core_num, void *stream);

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_LLAMA_KERNEL_ENCODER_VECTOR_KERNELS_H_
