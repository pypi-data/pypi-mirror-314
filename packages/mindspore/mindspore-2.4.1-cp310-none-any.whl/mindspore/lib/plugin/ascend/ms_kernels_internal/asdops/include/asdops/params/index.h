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
#ifndef ASDOPS_PARAMS_INDEX_H
#define ASDOPS_PARAMS_INDEX_H

#include <string>
#include <sstream>

namespace AsdOps {
namespace OpParam {
struct Index {
    enum IndexType {
        INDEX_UNDEFINED = 0,
        INDEX_ADD,
    };
    IndexType indexType;
    int64_t axis = 0;

    bool operator==(const Index &other) const
    {
        return (this->indexType == other.indexType) && (this->axis == other.axis);
    };
};
} // namespace OpParam
} // namespace AsdOps

#endif