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
#ifndef MS_OP_LOG_LOGSINK_H
#define MS_OP_LOG_LOGSINK_H

#include <fstream>
#include <mutex>
#include "utils/log/log_entity.h"

namespace mindspore {
namespace internal {
class LogSink {
 public:
  LogSink() = default;
  virtual ~LogSink() = default;
  virtual void Log(const char *log, uint64_t logLen) = 0;
};

class LogSinkStdout : public LogSink {
 public:
  LogSinkStdout() = default;
  ~LogSinkStdout() override = default;
  void Log(const char *log, uint64_t logLen) override;

 private:
  std::mutex mtx_;
};

class LogSinkFile : public LogSink {
 public:
  LogSinkFile();
  ~LogSinkFile() override;
  void Log(const char *log, uint64_t logLen) override;

 private:
  LogSinkFile(const LogSinkFile &) = delete;
  const LogSinkFile &operator=(const LogSinkFile &) = delete;
  void Init();
  void OpenFile();
  void DeleteOldestFile();
  std::string GetNewLogFilePath();
  bool IsDiskAvailable();
  void MakeLogDir();
  void CloseFile();
  std::string GetHomeDir();

 private:
  std::string boostType_;
  std::string logDir_;
  int currentFd_ = -1;
  uint64_t currentFileSize_ = 0;
  std::mutex mutex_;
};
}  // namespace internal
}  // namespace mindspore
#endif