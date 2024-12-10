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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_REGISTER_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_REGISTER_H_

#include <vector>

namespace mindspore {
namespace acme {

extern const char *kMatmulKernelName;
extern const char *kMultiWeightMatmulKernelName;
extern const size_t kFlashAttentionScoreRegisterIndex;
extern const size_t kPagedAttentionRegisterIndex;
extern const std::vector<std::vector<const char *>> kKernelMaps;

class KernelRegister {
 public:
  KernelRegister();
  ~KernelRegister() = default;

  static const KernelRegister &GetInstance() {
    static const KernelRegister kKernelRegister;
    return kKernelRegister;
  }

  void Register();
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_KERNEL_REGISTER_H_