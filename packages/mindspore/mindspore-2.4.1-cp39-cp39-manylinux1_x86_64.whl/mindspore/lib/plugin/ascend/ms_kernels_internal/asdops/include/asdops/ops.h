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
#ifndef ASDOPS_OPS_H
#define ASDOPS_OPS_H
#include <vector>
#include <string>
#include <memory>
#include "asdops/tensor.h"
#include "asdops/op_desc.h"
#include "asdops/run_info.h"
#include "asdops/operation.h"
#include "asdops/tactic.h"

namespace AsdOps {
class OpSchedule;

class Ops {
public:
    /**
     * @brief Return the singleton object
     *
     * @return Ops&
     */
    static Ops &Instance();
    /**
     * @brief Get the All Operations object
     *
     * @param[std::vector<Operation *> &] ops
     */
    void GetAllOperations(std::vector<Operation *> &ops) const;
    /**
     * @brief Get the Operation By Name object
     *
     * @param[const std::string&] opName
     * @return Operation*
     */
    Operation *GetOperationByName(const std::string &opName) const;
    /**
     * @brief Get the Operation By Id object
     *
     * @param[uint64_t] opId
     * @return Operation*
     */
    Operation *GetOperationById(uint64_t opId) const;
    /**
     * @brief Get the Tactic By Name object
     *
     * @param[const std::string &] tacticName
     * @return Tactic*
     */
    Tactic *GetTacticByName(const std::string &tacticName) const;
    /**
     * @brief Get the Tactic By Id object
     *
     * @param[uint64_t] tacticId
     * @return Tactic*
     */
    Tactic *GetTacticById(uint64_t tacticId) const;

private:
    Ops();
    ~Ops();

private:
    std::unique_ptr<OpSchedule> opSchedule_;
};
} // namespace AsdOps

#endif