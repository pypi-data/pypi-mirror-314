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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ADD_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ADD_IMPL_H_

#include <vector>

#include "include/internal_kernel.h"

#include "asdops/types.h"
#include "tiling/add_tiling.h"

namespace mindspore {
namespace internal {
// constexpr uint32_t MAX_AVAILABLE_UB_910B = 24568;
// constexpr uint32_t MULTI_CORE_THRESHOLD = 32 * 2;
// constexpr uint32_t MATCH_FACTOR = 4;
class AddImpl : public InternelKernelImpl {
 public:
  AddImpl(const OpParamPtr &param) : InternelKernelImpl(param) {}
  virtual ~AddImpl() {}
  bool Init(const ValidateInfo &info) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  size_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;
  bool IsSupported() override;

 private:
  void NoBroadCastTiling(AddTilingData *tiling);
  void BroadCastDim0Tiling(AddTilingData *tiling);
  DeviceRawBuf tiling_buf_;
  std::string soc_{"Ascend910B2"};
  bool same_shape{true};
  DIMS input_shape1;
  DIMS input_shape2;
  uint32_t dim_axis{0};
};
}  // namespace internal
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ADD_IMPL_H_