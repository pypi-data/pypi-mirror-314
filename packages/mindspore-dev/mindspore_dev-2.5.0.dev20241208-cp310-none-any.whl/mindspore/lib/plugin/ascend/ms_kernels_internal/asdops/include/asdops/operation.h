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
#ifndef ASDOPS_OPERATION_H
#define ASDOPS_OPERATION_H

#include <string>
#include <vector>
#include "asdops/launch_param.h"
#include "asdops/tactic.h"
#include "asdops/utils/status/status.h"

namespace AsdOps {
class Operation {
public:
    Operation() = default;
    virtual ~Operation() = default;
    virtual std::string GetName() const = 0;
    virtual uint64_t GetId() const = 0;
    virtual void GetAllTacticNames(std::vector<std::string> &tacticNames) const = 0;
    virtual void GetAllTactics(std::vector<Tactic *> &tactics) const = 0;
    virtual AsdOps::Status InferShape(LaunchParam &launchParam) const = 0;
    virtual void GetValidTactics(const LaunchParam &launchParam, std::vector<Tactic *> &validTactics) const = 0;
    virtual Tactic *GetBestTactic(const LaunchParam &launchParam) const = 0;
    virtual uint64_t GetTacticCount() const = 0;
    virtual Tactic *GetTacticByName(const std::string &tacticName) const = 0;
    virtual Tactic *GetTacticById(uint64_t tacticId) const = 0;
    virtual int64_t GetInputNum(const OpDesc &opDesc) const = 0;
    virtual int64_t GetOutputNum(const OpDesc &opDesc) const = 0;
    virtual bool IsConsistent(const LaunchParam &launchParam) const = 0;
};
} // namespace AsdOps

#endif