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
#ifndef ASDOPS_PARAMS_NORM_H
#define ASDOPS_PARAMS_NORM_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"
#include "asdops/utils/compare/compare.h"

namespace AsdOps {
namespace OpParam {
struct Norm {
    enum NormType { NORM_UNDEFINED = 0, LAYER_NORM, RMS_NORM, RMS_NORM_FORWARD, RMS_NORM_BACKWARD};
    NormType normType;
    // layernorm
    int32_t beginNormAxis = 0;
    int32_t beginParamsAxis = 0;
    // postlayernorm
    // opsMode = 0 : high precision
    // opsMode = 1 : high performance
    size_t opsMode = 0;
    float epsilon = 0.1f;
    float zoomScaleValue = 1.0f;
    // post/pre rmsnorm
    // precisionMode = 0 : high precision(weight fp32)
    // precisionMode = 1 : high performance(weight fp16)
    uint32_t precisionMode = 0;
    uint32_t gemmaMode = 0;
    bool inGamma = false; // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic, PostLayernormF16Tactic,
                          // LayernormF16QuantTactic, PostLayernormF16QuantTactic, RmsPreNormQuantTactic, RmsNormTactic,
                          // RmsNormQuantTactic
    bool inBeta = false;  // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic, PostLayernormF16Tactic,
                          // LayernormF16QuantTactic, PostLayernormF16QuantTactic, RmsNormQuantTactic
    bool inRes = false;   // PostLayernormF16Tactic, PostLayernormF16QuantTactic, RmsPreNormQuantTactic
    bool inNormBias = false;  // RmsPreNormQuantTactic
    bool outMean = false;     // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic
    bool outVarience = false; // LayernormF16Tactic, LayernormBF16Tactic, LayernormF32Tactic
    bool outResQuant = false; // LayernormF16QuantTactic, PostLayernormF16QuantTactic
    bool outRes = false;      // RmsPreNormQuantTactic
    bool isDynamicQuant = false; // rmsnorm + dynamicquant、layernorm + dynamicquant
    bool isSymmetric = true; // symmetric or asymmetric

    bool operator==(const Norm &other) const
    {
        return this->normType == other.normType && this->beginNormAxis == other.beginNormAxis &&
               this->beginParamsAxis == other.beginParamsAxis && this->opsMode == other.opsMode &&
               Utils::Compare<float>::IsEqual(this->epsilon, other.epsilon) &&
               Utils::Compare<float>::IsEqual(this->zoomScaleValue, other.zoomScaleValue) &&
               this->inGamma == other.inGamma &&
               this->inBeta == other.inBeta &&
               this->inRes == other.inRes &&
               this->inNormBias == other.inNormBias &&
               this->outMean == other.outMean &&
               this->outVarience == other.outVarience &&
               this->outResQuant == other.outResQuant &&
               this->outRes == other.outRes &&
               this->precisionMode == other.precisionMode &&
               this->gemmaMode == other.gemmaMode &&
               this->isDynamicQuant == other.isDynamicQuant;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif