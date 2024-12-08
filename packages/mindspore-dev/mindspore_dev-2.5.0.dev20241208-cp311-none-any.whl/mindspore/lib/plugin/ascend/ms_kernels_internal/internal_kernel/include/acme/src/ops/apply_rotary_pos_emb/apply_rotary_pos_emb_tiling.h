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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_APPLY_ROTARY_POS_EMB_APPLY_ROTARY_POS_EMB_TILING_H
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_APPLY_ROTARY_POS_EMB_APPLY_ROTARY_POS_EMB_TILING_H

#include <sstream>
#include <stdint.h>
#include "utils/log/log.h"
#include "acme/include/op_param.h"
#include "apply_rotary_pos_emb_tiling_data.h"

namespace mindspore {
namespace acme {
static std::ostringstream &operator<<(std::ostringstream &os, const RopeTilingData &dt) {
  os << "RopeTilingData: hiddenSizeQ:" << dt.hiddenSizeQ << ", hiddenSizeK:" << dt.hiddenSizeK
     << ", headDim:" << dt.headDim << ", headNumQ:" << dt.headNumQ << ", headNumK:" << dt.headNumK
     << ", rotaryCoeff:" << dt.rotaryCoeff << ", ntokens:" << dt.ntokens << ", realCore:" << dt.realCore
     << ", cosFormat:" << dt.cosFormat << ", batch:" << dt.batch << ", maxUbSize:" << dt.maxUbSize
     << ", tilingId:" << dt.tilingId << ", seqLen:" << dt.seqLen << ", broadCastCos:" << dt.broadCastCos
     << ", posDtype:" << dt.posDtype << ", posSize:" << dt.posSize << ", maxSeqLen:" << dt.maxSeqLen;
  return os;
}
AcmeStatus RopeTilingImpl(RawHostAddr &host_ptr, const InputsDescList &inputs, uint64_t *workspaceSize,
                          bool isAscend310p, const ApplyRotaryPosEmbParam &param);
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_APPLY_ROTARY_POS_EMB_APPLY_ROTARY_POS_EMB_TILING_H
