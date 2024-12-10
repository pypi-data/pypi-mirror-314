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
#ifndef ASDOPS_TENSORDESC_H
#define ASDOPS_TENSORDESC_H
#include "asdops/types.h"
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
struct TensorDesc {
    TensorDType dtype = TENSOR_DTYPE_UNDEFINED;
    TensorFormat format = TENSOR_FORMAT_UNDEFINED;
    AsdOps::SVector<int64_t> dims;
    int64_t Numel() const;
    void View(const AsdOps::SVector<int64_t> &newDims);
    void CombinDim(size_t fromDimPos, size_t endDimPos);
    void EraseFirstDimOne(); // 删除Dim等于1的第一个维度
    void AddDimOne();
    std::string ToString() const;
};
} // namespace AsdOps

#endif