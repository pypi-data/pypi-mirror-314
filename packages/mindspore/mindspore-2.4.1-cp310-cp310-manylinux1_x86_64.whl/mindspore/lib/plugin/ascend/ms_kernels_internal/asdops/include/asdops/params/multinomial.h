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
#ifndef ASDOPS_PARAMS_MULTINOMIAL_H
#define ASDOPS_PARAMS_MULTINOMIAL_H

#include <string>
#include <sstream>

namespace AsdOps {
namespace OpParam {
struct Multinomial {
    uint32_t numSamples = 1;
    uint32_t randSeed = 0;
    bool operator==(const Multinomial &other) const
    {
        if (this->randSeed == 0xffffffff || other.randSeed == 0xffffffff) {
            return false;
        }
        return (this->numSamples == other.numSamples) && (this->randSeed == other.randSeed);
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif