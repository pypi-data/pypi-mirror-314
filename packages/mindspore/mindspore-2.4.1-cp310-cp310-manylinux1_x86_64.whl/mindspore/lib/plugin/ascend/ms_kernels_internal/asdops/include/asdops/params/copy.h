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

#ifndef ASDOPS_PARAMS_COPY_H
#define ASDOPS_PARAMS_COPY_H

#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
namespace OpParam {
struct Copy {
    SVector<int64_t> dstSize;
    SVector<int64_t> dstStride;
    SVector<int64_t> dstOffset;

    bool operator==(const Copy &other) const
    {
        return this->dstSize == other.dstSize && this->dstStride == other.dstStride &&
               this->dstOffset == other.dstOffset;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif