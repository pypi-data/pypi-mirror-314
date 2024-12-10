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
#ifndef MS_OP_LOG_LOGENTITY_H
#define MS_OP_LOG_LOGENTITY_H
#include <chrono>
#include <string>
#include <vector>

namespace mindspore {
namespace internal {
enum class LogLevel { DEBUG = 0, INFO, WARN, ERROR, EXCEPTION };

const char *LogLevelToString(LogLevel level);

struct LogEntity {
  std::chrono::system_clock::time_point time;
  long threadId = 0;
  LogLevel level = LogLevel::WARN;
  const char *fileName = nullptr;
  int line = 0;
  const char *funcName = nullptr;
};
}  // namespace internal
}  // namespace mindspore
#endif