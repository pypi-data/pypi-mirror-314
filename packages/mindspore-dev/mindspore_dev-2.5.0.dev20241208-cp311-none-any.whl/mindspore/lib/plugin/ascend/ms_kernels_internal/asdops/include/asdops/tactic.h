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
#ifndef ASDOPS_TACTIC_H
#define ASDOPS_TACTIC_H

#include <string>
#include <vector>
#include "asdops/launch_param.h"
#include "asdops/run_info.h"
#include "asdops/utils/status/status.h"

namespace AsdOps {
class Tactic {
public:
    Tactic() = default;
    virtual ~Tactic() = default;
    virtual std::string GetName() const = 0;
    virtual uint64_t GetId() const = 0;

    virtual bool CanSupport(const LaunchParam &launchParam) const = 0;

    virtual uint64_t GetTilingSize(const LaunchParam &launchParam) const = 0;
    virtual Status InitRunInfo(const LaunchParam &launchParam, RunInfo &runInfo) const = 0;
    virtual Status Run(const LaunchParam &launchParam, RunInfo &runInfo) = 0;

    virtual bool Serialize(std::vector<char> &hostCode, std::vector<char> &deviceCode) = 0;

    enum OpType {
        OP_TYPE_AI_CORE = 0,
        OP_TYPE_AI_CPU,
        OP_TYPE_AIV,
        OP_TYPE_WRITE_BACK,
        OP_TYPE_MIX_AIC,
        OP_TYPE_MIX_AIV,
        OP_TYPE_FFTS_PLUS,
        OP_TYPE_DSA,
        OP_TYPE_DVPP,
        OP_TYPE_HCCL,
        OP_TYPE_INVALID
    };
    virtual OpType GetType() const = 0;
};
} // namespace AsdOps

#endif