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
#ifndef MS_KERNELS_INTERNAL_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_H_
#include <memory>
#include <vector>
#include "ms_int_types.h"
#include "op_param.h"
#include "internal_rtbackend.h"

namespace mindspore {
namespace internal {

struct RawBuf {
  uint64_t size_{0};
  void *addr_{nullptr};
};
using HostRawBuf = RawBuf;
using DeviceRawBuf = RawBuf;

using OpParamPtr = std::shared_ptr<OpParam>;
using DtypesParamPtr = std::shared_ptr<DtypesParam>;

struct ValidateInfo {
  size_t input_num_;
  size_t output_num_;
  std::vector<TensorDType> input_dtype_;
  std::vector<TensorDType> output_dtype_;
  std::vector<TensorFormat> input_format_;
  std::vector<TensorFormat> output_format_;
};

class InternelKernelImpl {
 public:
  InternelKernelImpl(const OpParamPtr &param) : param_(param) {};
  virtual ~InternelKernelImpl();
  // this routine will check if this kernel can support the requirements
  // specified in ValidationInfo.
  virtual bool Init(const ValidateInfo &) = 0;
  virtual void SetInputs(const std::vector<Tensor *> &inputs);
  virtual void SetOutputs(const std::vector<Tensor *> &outputs);
  virtual void SetWorkSpace(const std::vector<DeviceRawBuf> &workspace);
  virtual void SetStream(const void *stream_ptr);
  virtual void SetDeviceTilingBuf(const DeviceRawBuf &tilingBuf) = 0;
  virtual int Launch() = 0;
  virtual uint64_t GetTilingBufSize() = 0;
  virtual int Tiling(HostRawBuf &tilingBuf) = 0;
  virtual std::vector<uint64_t> GetWorkSpaceSize() = 0;
  virtual int InferShape(const std::vector<DIMS> &input_shapes, std::vector<DIMS> &output_shapes) = 0;
  virtual bool IsSupported() { return true; }
  virtual std::string GetOpName();
  virtual uint32_t GetLaunchCoreNum();

  virtual CacheInfo &GetCacheInfo() { return cache_info_; }

  virtual void SetCacheInfo(const CacheInfo &cache_info) { cache_info_ = cache_info; }

  virtual void UpdateParam(const OpParamPtr &param) { return; };

  void GetRtFunction();
  int LaunchOperator();

 protected:
  OpParamPtr param_ = nullptr;
  std::vector<Tensor *> inputs_;
  std::vector<Tensor *> outputs_;
  void *stream_ptr_ = nullptr;

  CacheInfo cache_info_;

  int status_ = INTERNAL_RTSUCCESS;
  void *soHandle_ = nullptr;
  RtDevBinaryRegisterFunc rtDevBinaryRegister_ = nullptr;
  RtFunctionRegisterFunc rtFunctionRegister_ = nullptr;
  RtKernelLaunchFunc rtKernelLaunch_ = nullptr;
  RtGetC2cCtrlAddrFunc rtGetC2cCtrlAddr_ = nullptr;

 private:
  virtual int LaunchWithProfiling();
};
using InternalKernelImplPtr = std::shared_ptr<InternelKernelImpl>;
InternalKernelImplPtr CreateInternalKernelImpl(const OpParamPtr &param);
bool IsInternalKernelDtypesSupported(const DtypesParamPtr &param);
}  // namespace internal
}  // namespace mindspore
#endif
