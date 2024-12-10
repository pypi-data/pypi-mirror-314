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
#ifndef ASDOPS_PARAMS_MATMUL_H
#define ASDOPS_PARAMS_MATMUL_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"
#include "asdops/types.h"

namespace AsdOps {
namespace OpParam {
struct MatMul {
    bool transposeA = false;
    bool transposeB = false;
    SVector<int64_t> oriShape = {0, 0, 0}; // original shape: m,k,n - (m,k) * (k,n)
    bool withBias = false;
    bool enDequant = false;
    uint32_t tilingN = 0;                        // 压缩算法透传参数, 单压缩块 n 方向的基块数
    uint32_t tilingK = 0;                        // 压缩算法透传参数, 单压缩块 k 方向的基块数
    bool enShuffleK = false;                     // Shuffle-K使能，默认关。
    TensorDType outDtype = TENSOR_DTYPE_FLOAT16; // 只有量化能用， 可选FLOAT16：1  BFLOAT16:27
    bool operator==(const MatMul &other) const
    {
        return this->transposeA == other.transposeA && this->transposeB == other.transposeB &&
               this->oriShape == other.oriShape && this->withBias == other.withBias &&
               this->enDequant == other.enDequant && this->tilingN == other.tilingN && this->tilingK == other.tilingK &&
               this->outDtype == other.outDtype;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif // ASDOPS_PARAMS_MATMUL_H