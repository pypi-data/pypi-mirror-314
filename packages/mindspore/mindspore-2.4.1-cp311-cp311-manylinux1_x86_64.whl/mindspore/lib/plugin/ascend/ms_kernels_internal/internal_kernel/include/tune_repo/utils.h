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
#ifndef TUNE_REPO_UTILS_H
#define TUNE_REPO_UTILS_H

#include <string>
#include <unordered_map>
#include <vector>
struct IntArrayHasher {
  std::size_t operator()(const std::vector<int> &arr) const {
    std::size_t hash = 0;
    for (int num : arr) {
      hash ^= std::hash<int>{}(num) + 0x9e3779b9 + (hash << 6) + (hash >> 2);
    }
    return hash;
  }
};

using REPO = std::unordered_map<std::vector<int>, std::vector<int>, IntArrayHasher>;

inline std::string GetStringEnv(const char *env_name) {
  const char *ret = getenv(env_name);
  return ret != nullptr ? std::string(ret) : std::string();
}

inline bool DisableRepo() { return GetStringEnv("DISABLE_REPO") == "1"; }

#endif  // TUNE_REPO_UTILS_H
