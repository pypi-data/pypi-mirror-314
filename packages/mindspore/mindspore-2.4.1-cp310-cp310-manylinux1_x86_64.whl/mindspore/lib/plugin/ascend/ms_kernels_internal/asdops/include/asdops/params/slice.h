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
#ifndef ASDOPS_PARAMS_SLICE_H
#define ASDOPS_PARAMS_SLICE_H

#include <cstdint>
#include <string>
#include <sstream>
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
namespace OpParam {
struct Slice {
    SVector<int64_t> offsets;
    SVector<int64_t> size;

    bool operator==(const Slice &other) const
    {
        return this->offsets == other.offsets && this->size == other.size;
    }
};
} // namespace OpParam
} // namespace AsdOps

#endif // ASDOPS_PARAMS_SLICE_H