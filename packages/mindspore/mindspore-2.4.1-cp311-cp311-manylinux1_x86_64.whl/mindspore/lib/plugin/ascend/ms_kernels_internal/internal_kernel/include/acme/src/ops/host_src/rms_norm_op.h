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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_RMSNORM_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_RMSNORM_OP_H_

#include <algorithm>
#include "acme/include/acme_op.h"
#include "acme/include/op_param.h"
#include "acme/include/base_type.h"
#include "acme/src/ops/host_src/multi_impls_op.h"

#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"
#include "asdops/params/norm.h"

namespace mindspore {
namespace acme {
class RmsNormOp : public MultiImplsOp {
 public:
  RmsNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
            const NormParam &param, const std::string &op_name);
  ~RmsNormOp() = default;

  AcmeStatus InitImpl() override;
  AsdOps::Any BuildAsdParam() override;
  const std::string &TargetKernelName() const override { return target_kernel_name; }
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  bool UseAsdopImpl() override;
  AcmeStatus TilingImplAcme(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImplAcme(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                            const WsAddrList &ws_ptrs, void *stream) override;
  std::string DumpTilingAcme(const RawHostAddr host_ptr) const override;
  uint32_t GetLaunchCoreNumAcme() const override;

 private:
  NormParam param_;
  bool is_ascend_310p_{false};
  const std::string target_kernel_name{"NormOperation"};
};

using RmsNormOpPtr = std::shared_ptr<RmsNormOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_RMSNORM_OP_H
