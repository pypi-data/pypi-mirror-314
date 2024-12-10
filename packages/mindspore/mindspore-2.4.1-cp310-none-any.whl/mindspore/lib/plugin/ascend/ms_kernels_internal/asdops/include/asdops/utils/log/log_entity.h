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
#ifndef COMMON_LOG_LOGENTITY_H
#define COMMON_LOG_LOGENTITY_H
#include <chrono>
#include <string>

namespace AsdOps {
enum class LogLevel { TRACE = 0, DEBUG, INFO, WARN, ERROR, FATAL };

const char *LogLevelToString(LogLevel level);

struct LogEntity {
    std::chrono::system_clock::time_point time;
    long threadId = 0;
    LogLevel level = LogLevel::TRACE;
    const char *fileName = nullptr;
    int line = 0;
    const char *funcName = nullptr;
};
} // namespace AsdOps
#endif