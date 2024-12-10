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
#ifndef MS_KERNELS_INTERNAL_KERNEL_ELEWISE_BINARY_IMPL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ELEWISE_BINARY_IMPL_H_

#include <vector>
#include "include/internal_kernel.h"
#include "include/param/elewise_param.h"

namespace mindspore {
namespace internal {
class ElewiseBinaryImpl : public InternelKernelImpl {
 public:
  ElewiseBinaryImpl(const OpParamPtr &param) : InternelKernelImpl(param) {}
  virtual ~ElewiseBinaryImpl() {}
  bool Init(const ValidateInfo &info) override;
  int Launch() { return -1; };
  int Tiling(HostRawBuf &tilingBuf) override;
  void SetStream(const void *stream_ptr) override;
  void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) override;
  uint64_t GetTilingBufSize() override;
  std::vector<uint64_t> GetWorkSpaceSize() override;
  int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) override;
  virtual int32_t GetMaxUbCount(uint32_t op_dtype);
  bool IsSupported() override;

 protected:
  void *stream_ptr_ = nullptr;
  uint8_t *device_tiling_ = nullptr;
  uint32_t aligned_factor_ = 128;
  uint32_t ub_dtype = 0;
};
}  // namespace internal
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_ELEWISE_BINARY_IMPL_H_