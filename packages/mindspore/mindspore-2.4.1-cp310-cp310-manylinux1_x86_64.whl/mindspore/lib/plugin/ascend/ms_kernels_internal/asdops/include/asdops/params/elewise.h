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
#ifndef ASDOPS_PARAMS_ELEWISE_H
#define ASDOPS_PARAMS_ELEWISE_H

#include "asdops/types.h"
#include "asdops/utils/compare/compare.h"

namespace AsdOps {
namespace OpParam {
struct Elewise {
    enum ElewiseType {
        ELEWISE_UNDEFINED = 0,
        ELEWISE_CAST,
        ELEWISE_MULS,
        ELEWISE_COS,
        ELEWISE_SIN,
        ELEWISE_NEG,
        ELEWISE_QUANT,
        ELEWISE_LOGICAL_NOT,
        ELEWISE_ADD,
        ELEWISE_MUL,
        ELEWISE_REALDIV,
        ELEWISE_LOGICAL_AND,
        ELEWISE_LOGICAL_OR,
        ELEWISE_LESS,
        ELEWISE_GREATER,
        ELEWISE_SUB,
        ELEWISE_TANH,
        ELEWISE_EQUAL,
        ELEWISE_QUANT_PER_CHANNEL,
        ELEWISE_DEQUANT_PER_CHANNEL,
        ELEWISE_DYNAMIC_QUANT,
    };
    ElewiseType elewiseType;

    float varAttr = 0.0f;    // MULS
    float inputScale = 1.0f; // QUANT
    int inputOffset = 0;     // QUANT
    bool asymmetric = false; // DynamicQuant false : symmetric，true : asymmetric
    TensorDType outTensorType = TENSOR_DTYPE_UNDEFINED;

    bool operator==(const Elewise &other) const
    {
        return this->elewiseType == other.elewiseType && Utils::Compare<float>::IsEqual(this->varAttr, other.varAttr) &&
               Utils::Compare<float>::IsEqual(this->inputScale, other.inputScale) &&
               this->inputOffset == other.inputOffset &&
               this->asymmetric == other.asymmetric &&
               this->outTensorType == other.outTensorType;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif
