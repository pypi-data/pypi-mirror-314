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
#ifndef ASDOPS_PARAMS_TRANSDATA_H
#define ASDOPS_PARAMS_TRANSDATA_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
namespace OpParam {
struct Transdata {
    enum TransdataType { UNDEFINED = 0, FRACTAL_NZ_TO_ND, ND_TO_FRACTAL_NZ };
    TransdataType transdataType = UNDEFINED;
    SVector<int64_t> outCrops = {0, 0};
    enum SpecialType { NORMAL = 0, ATTENTION_INPUT_QKV, ATTENTION_INPUT_MASK};
    int64_t specialTransdata = NORMAL;

    bool operator==(const Transdata &other) const
    {
        return this->transdataType == other.transdataType && this->outCrops == other.outCrops;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif // ASDOPS_PARAMS_TRANSDATA_H