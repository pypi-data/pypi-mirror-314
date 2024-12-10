/**
 * Copyright 2023-2024 Huawei Technologies Co., Ltd
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
#ifndef MS_KERNELS_INTERNAL_TYPES_H_
#define MS_KERNELS_INTERNAL_TYPES_H_
#include "asdops/types.h"
#include "asdops/tensor_desc.h"
#include "asdops/tensor.h"
#include "asdops/run_info.h"
#include <memory>
#include <vector>
namespace mindspore {
namespace internal {
using TensorDesc = AsdOps::TensorDesc;
using Tensor = AsdOps::Tensor;
using TensorFormat = AsdOps::TensorFormat;
using TensorDType = AsdOps::TensorDType;
using DIMS = AsdOps::SVector<int64_t>;
using RunInfo = AsdOps::RunInfo;

struct TilingCacheInfo {
  RunInfo run_info_;
  uint64_t workspace_size_{0};
  uint32_t core_num_{1};
  uint32_t cache_id_{1};
  bool use_asd_tiling_{false};

  TilingCacheInfo() {}

  TilingCacheInfo(const TilingCacheInfo &other) {
    if (other.use_asd_tiling_) {
      other.run_info_.CopyTo(this->run_info_);
    }
    this->workspace_size_ = other.workspace_size_;
    this->core_num_ = other.core_num_;
    this->cache_id_ = other.cache_id_;
    this->use_asd_tiling_ = other.use_asd_tiling_;
  }

  const TilingCacheInfo &operator=(const TilingCacheInfo &other) {
    if (other.use_asd_tiling_) {
      other.run_info_.CopyTo(this->run_info_);
    }
    this->workspace_size_ = other.workspace_size_;
    this->core_num_ = other.core_num_;
    this->cache_id_ = other.cache_id_;
    this->use_asd_tiling_ = other.use_asd_tiling_;
    return *this;
  }

  AsdOps::KernelInfo &GetKernelInfo() { return run_info_.GetKernelInfo(); }
  void SetAsdTiling() { use_asd_tiling_ = true; }
};

using CacheInfo = TilingCacheInfo;

template <typename T>
std::vector<T> SVecToVec(const AsdOps::SVector<T> &sv) {
  std::vector<T> v(sv.size());
  for (size_t i = 0; i < sv.size(); ++i) {
    v[i] = sv[i];
  }
  return v;
}

template <typename T>
AsdOps::SVector<T> VecToSVec(const std::vector<T> &v) {
  AsdOps::SVector<T> sv;
  for (size_t i = 0; i < v.size(); ++i) {
    sv.emplace_back(v[i]);
  }
  return sv;
}

inline DIMS ToDims(std::vector<int64_t> shape) { return VecToSVec<int64_t>(shape); }

}  // namespace internal
}  // namespace mindspore
#endif