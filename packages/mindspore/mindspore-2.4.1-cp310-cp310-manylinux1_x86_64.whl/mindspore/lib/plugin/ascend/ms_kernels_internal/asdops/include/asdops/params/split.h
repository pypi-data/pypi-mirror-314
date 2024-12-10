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
#ifndef ASDOPS_PARAMS_SPLIT_H
#define ASDOPS_PARAMS_SPLIT_H

namespace AsdOps {
namespace OpParam {
struct Split {
    int splitDim = 0;
    int splitNum = 2;

    bool operator==(const Split &other) const
    {
        return this->splitDim == other.splitDim && this->splitNum == other.splitNum;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif