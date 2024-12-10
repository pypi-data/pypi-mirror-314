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
#ifndef COMMON_NONCOPYABLE_NONCOPYABLE_H
#define COMMON_NONCOPYABLE_NONCOPYABLE_H

namespace AsdOps {
class NonCopyable {
protected:
    NonCopyable() = default;
    ~NonCopyable() = default;

private:
    NonCopyable(const NonCopyable &) = delete;
    const NonCopyable &operator=(const NonCopyable &) = delete;
};
} // namespace AsdOps
#endif