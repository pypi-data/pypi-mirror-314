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
#ifndef MS_KERNELS_INTERNAL_KERNEL_SUB_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_SUB_IMPL_H_

#include <vector>
#include "include/internal_kernel.h"
#include "asdops/types.h"

namespace mindspore {
namespace internal {
class SubImpl : public InternelKernelImpl {
 public:
  SubImpl(const OpParamPtr &param) : InternelKernelImpl(param) {}
  virtual ~SubImpl() {}
  bool Init(const ValidateInfo &info) override;
  void SetStream(const void *stream_ptr) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  int Launch() override;
  uint64_t GetTilingBufSize() override;
  int Tiling(HostRawBuf &tilingBuf) override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;
  bool IsSupported();

 private:
  int32_t GetMaxUbCount(uint32_t in_dtype);

 private:
  void *stream_ptr_ = nullptr;
  uint8_t *device_tiling_ = nullptr;
};
}  // namespace internal
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ADD_IMPL_H_