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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_ACME_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_ACME_OP_H_

#include <vector>
#include <string>
#include "acme/include/base_type.h"
#include "acme/include/op_param.h"
#include "acme/include/tiling_info.h"
#include "acme/src/core/dtype_registry.h"

namespace mindspore {
namespace acme {
class AcmeOp {
 public:
  AcmeOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
         const std::string &op_name);
  virtual ~AcmeOp() = default;
  AcmeStatus Init();

  virtual AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape);
  virtual AcmeStatus UpdateParam(const void *) { return kAcmeOk; }

  size_t GetTilingSize() const;
  virtual std::vector<size_t> GetWorkspaceSize() const;

  virtual void SetTilingInfo(const TilingInfoPtr &tiling_info);

  AcmeStatus Launch(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                    void *stream, const std::string &op_fullname = "");
  AcmeStatus Tiling(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr);
  virtual std::string DumpTiling(const RawHostAddr host_ptr) const = 0;

  virtual ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const = 0;

  virtual AcmeStatus TilingFromTuning(const RawDeviceAddr tiling_addr);
  virtual bool IsSupported(const InputDataTypes &dtypes);

  virtual std::string GetOpName() { return "Acme" + op_name_; };
  std::string GetOpNameOrigin() { return op_name_; };
  virtual uint32_t GetLaunchCoreNum() const { return host_run_info_comm_ptr_->block_dims_; };

 protected:
  virtual AcmeStatus InitImpl();
  virtual AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) = 0;
  virtual AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                                const WsAddrList &ws_ptrs, void *stream) = 0;
  void SetHostRunInfoComm(const HostRunInfoComm &, HostRunInfoPtr *);
  InputsDescList inputs_;
  OutputsDescList outputs_;
  std::string op_name_{"UnknownOp"};
  size_t tiling_size_{0};
  std::vector<size_t> ws_size_;
  RawDeviceAddr tiling_device_addr_{nullptr};
  std::string soc_;
  HostRunInfoCommPtr host_run_info_comm_ptr_{nullptr};

 private:
  virtual AcmeStatus LaunchWithProfiling(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                                         const WsAddrList &ws_ptrs, void *stream, const std::string &op_fullname);
};

using AcmeOpPtr = std::shared_ptr<AcmeOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_ACME_OP_H_