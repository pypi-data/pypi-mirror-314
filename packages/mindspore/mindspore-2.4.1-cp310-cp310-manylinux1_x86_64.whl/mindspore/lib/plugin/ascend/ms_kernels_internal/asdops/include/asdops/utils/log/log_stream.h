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
#ifndef COMMON_LOG_LOGSTREAM_H
#define COMMON_LOG_LOGSTREAM_H
#include <sstream>
#include "asdops/utils/log/log_entity.h"

namespace AsdOps {
class LogStream {
public:
    LogStream(const char *filePath, int line, const char *funcName, LogLevel level);
    ~LogStream();
    template <typename T> LogStream &operator<<(const T &value)
    {
        stream_ << value;
        return *this;
    }
    void Format(const char *format, ...);

private:
    LogEntity logEntity_;
    bool useStream_ = true;
    std::ostringstream &stream_;
};
} // namespace AsdOps
#endif