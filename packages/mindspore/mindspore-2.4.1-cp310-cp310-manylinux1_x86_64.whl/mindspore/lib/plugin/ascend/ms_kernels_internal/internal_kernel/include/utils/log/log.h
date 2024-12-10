/**
 * Copyright 2024 Huawei Technologies Co., Ltd
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
#ifndef MS_OP_LOG_H
#define MS_OP_LOG_H
#include "utils/log/log_stream.h"
#include "utils/log/log_core.h"
#include "utils/log/log_sink.h"
#include "utils/log/log_entity.h"
#include "utils/log/log_tiling.h"
#include "utils/log/log_utils.h"

#define MSOP_LOG(level) MSOP_LOG_##level

#define MSOP_FLOG(level, format, ...) MSOP_FLOG_##level(format, __VA_ARGS__)

#define MSOP_LOG_IF(condition, level) \
  if (condition) MSOP_LOG(level)

#define MSOP_LOG_DEBUG                                                                                \
  if (mindspore::internal::LogLevel::DEBUG >= mindspore::internal::LogCore::Instance().GetLogLevel()) \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::DEBUG)
#define MSOP_LOG_INFO                                                                                \
  if (mindspore::internal::LogLevel::INFO >= mindspore::internal::LogCore::Instance().GetLogLevel()) \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::INFO)
#define MSOP_LOG_WARNING                                                                             \
  if (mindspore::internal::LogLevel::WARN >= mindspore::internal::LogCore::Instance().GetLogLevel()) \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::WARN)
#define MSOP_LOG_ERROR                                                                                \
  if (mindspore::internal::LogLevel::ERROR >= mindspore::internal::LogCore::Instance().GetLogLevel()) \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::ERROR)
#define MSOP_LOG_EXCEPTION                                                                                \
  if (mindspore::internal::LogLevel::EXCEPTION >= mindspore::internal::LogCore::Instance().GetLogLevel()) \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::EXCEPTION)

#define MSOP_FLOG_DEBUG(format, ...)                                                                     \
  if (mindspore::internal::LogLevel::DEBUG >= mindspore::internal::LogCore::Instance().GetLogLevel())    \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::DEBUG) \
    .Format(format, __VA_ARGS__)
#define MSOP_FLOG_INFO(format, ...)                                                                     \
  if (mindspore::internal::LogLevel::INFO >= mindspore::internal::LogCore::Instance().GetLogLevel())    \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::INFO) \
    .Format(format, __VA_ARGS__)
#define MSOP_FLOG_WARNING(format, ...)                                                                  \
  if (mindspore::internal::LogLevel::WARN >= mindspore::internal::LogCore::Instance().GetLogLevel())    \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::WARN) \
    .Format(format, __VA_ARGS__)
#define MSOP_FLOG_ERROR(format, ...)                                                                     \
  if (mindspore::internal::LogLevel::ERROR >= mindspore::internal::LogCore::Instance().GetLogLevel())    \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::ERROR) \
    .Format(format, __VA_ARGS__)
#define MSOP_FLOG_EXCEPTION(format, ...)                                                                     \
  if (mindspore::internal::LogLevel::EXCEPTION >= mindspore::internal::LogCore::Instance().GetLogLevel())    \
  mindspore::internal::LogStream(__FILE__, __LINE__, __FUNCTION__, mindspore::internal::LogLevel::EXCEPTION) \
    .Format(format, __VA_ARGS__)

#endif