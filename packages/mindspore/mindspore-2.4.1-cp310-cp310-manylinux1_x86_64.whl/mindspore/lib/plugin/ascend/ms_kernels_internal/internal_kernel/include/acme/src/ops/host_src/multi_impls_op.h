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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MULTI_IMPLS_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MULTI_IMPLS_OP_H_

#include <any>
#include "acme/src/ops/host_src/asd_op_base.h"

namespace mindspore {
namespace acme {
class MultiImplsOp : public AcmeOp {
 public:
  MultiImplsOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
               const std::string &op_name);
  ~MultiImplsOp() = default;

  AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape) override;
  void SetTilingInfo(const TilingInfoPtr &tiling_info) override;

  virtual AsdOps::Any BuildAsdParam() = 0;
  virtual bool UseAsdop();
  virtual const std::string &TargetKernelName() const;
  virtual AsdOpPtr CreateAsdKernel(const InputsImmutableInfoList &inputs_ii,
                                       const OutputsImmutableInfoList &outputs_ii, const std::string &op_name,
                                       const AsdOps::Any &param, const std::string &kernel_name);
  std::string DumpTiling(const RawHostAddr host_ptr) const override;
  uint32_t GetLaunchCoreNum() const override;
  std::string GetOpName() override;

 protected:
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;

  virtual bool UseAsdopImpl() = 0;
  virtual AcmeStatus TilingImplAcme(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) = 0;
  virtual AcmeStatus LaunchImplAcme(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                                         const WsAddrList &ws_ptrs, void *stream) = 0;
  virtual std::string DumpTilingAcme(const RawHostAddr host_ptr) const = 0;
  virtual uint32_t GetLaunchCoreNumAcme() const = 0;
  AsdOpPtr asd_op_{nullptr};
  bool use_asdop_{false};
  bool init_asdop_{false};
  bool is_enabled_env_{false};
};

}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MULTI_IMPLS_OP_H_