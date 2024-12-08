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
#ifndef CORE_BASE_OPERATION_REGISTER_H
#define CORE_BASE_OPERATION_REGISTER_H

#include <map>
#include <vector>

#include "asdops/operation.h"
#include "asdops/tactic.h"
#include "asdops/utils/assert/assert.h"
#include "asdops/utils/log/log.h"

namespace AsdOps {
using NewOperationFunc = Operation*(*)();
using NewTacticFunc = Tactic*(*)();

class OperationRegister {
public:
    OperationRegister(const char *opName, NewOperationFunc func) noexcept
    {
        ASDOPS_CHECK(opName != nullptr, "opName is nullptr", return);
        auto &operationCreators = OperationCreators();
        operationCreators.push_back(func);
        ASD_LOG(DEBUG) << "register operation " << opName;
    }

    OperationRegister(const char *opName, const char *tacName, NewTacticFunc func) noexcept
    {
        ASDOPS_CHECK(opName != nullptr, "opName is nullptr", return);
        ASDOPS_CHECK(tacName != nullptr, "tacName is nullptr", return);
        auto &tacticCreators = TacticCreators();
        tacticCreators[func] = opName;
        ASD_LOG(DEBUG) << "register tactic " << tacName << " of operation " << opName;
    }

    static std::vector<NewOperationFunc> &OperationCreators()
    {
        static std::vector<NewOperationFunc> operationCreators;
        return operationCreators;
    }

    static std::map<NewTacticFunc, std::string> &TacticCreators()
    {
        static std::map<NewTacticFunc, std::string> tacticCreators;
        return tacticCreators;
    }
};

#define REG_OPERATION(opName)                                                   \
    Operation *GetOperation##opName()                                           \
    {                                                                           \
        static opName op##opName(#opName);                                      \
        return &op##opName;                                                     \
    }                                                                           \
    static OperationRegister opName##register =                                 \
        OperationRegister(#opName, GetOperation##opName)

#define REG_TACTIC(tacName)                                                     \
    Tactic *GetTactic##tacName()                                                \
    {                                                                           \
        static tacName tac##tacName(#tacName);                                  \
        return &tac##tacName;                                                   \
    }                                                                           \
    static OperationRegister tacName##register =                                \
        OperationRegister(OperationPlaceHolder, #tacName, GetTactic##tacName)
}

#endif