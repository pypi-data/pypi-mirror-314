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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ROPE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ROPE_H_

#include "include/internal_kernel.h"
#include <vector>
#include "kernel/apply_rotary_pos_emb_tiling.h"

namespace mindspore {
namespace internal {
class ApplyRotaryPosEmbImpl : public InternelKernelImpl {
 public:
  ApplyRotaryPosEmbImpl(const OpParamPtr &param) : InternelKernelImpl(param) {}
  virtual ~ApplyRotaryPosEmbImpl() {}
  bool Init(const ValidateInfo &info) override;
  void SetWorkSpace(const std::vector<DeviceRawBuf> &workspace) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  uint64_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;

 protected:
  void SetTilingID(RopeTilingData *tiling, int typeKey);
  DeviceRawBuf tiling_buf_;
  DeviceRawBuf workSpace_buf_;
  std::string soc_{"Ascend910B2"};
};
}  // namespace internal
}  // namespace mindspore
#endif