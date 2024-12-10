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
#ifndef COMMON_LOG_LOGSINK_H
#define COMMON_LOG_LOGSINK_H
#include "asdops/utils/log/log_entity.h"

namespace AsdOps {
class LogSink {
public:
    LogSink() = default;
    virtual ~LogSink() = default;
    virtual void Log(const char *log, uint64_t logLen) = 0;
};
} // namespace AsdOps
#endif