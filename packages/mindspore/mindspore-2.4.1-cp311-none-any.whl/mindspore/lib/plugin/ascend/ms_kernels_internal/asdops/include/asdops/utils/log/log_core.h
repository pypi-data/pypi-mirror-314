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
#ifndef COMMON_LOG_LOGCORE_H
#define COMMON_LOG_LOGCORE_H
#include <memory>
#include <vector>
#include "asdops/utils/log/log_entity.h"
#include "asdops/utils/log/log_sink.h"
#include "asdops/utils/svector/svector.h"

namespace AsdOps {
class LogCore {
public:
    LogCore();
    virtual ~LogCore() = default;
    static LogCore &Instance();
    LogLevel GetLogLevel() const;
    void SetLogLevel(LogLevel level);
    void Log(const char *log, uint64_t logLen);
    void DeleteLogFileSink();
    void AddSink(std::shared_ptr<LogSink> sink);
    const std::vector<std::shared_ptr<LogSink>> &GetAllSinks() const;

private:
    std::vector<std::shared_ptr<LogSink>> sinks_;
    LogLevel level_ = LogLevel::INFO;
};
} // namespace AsdOps
#endif
