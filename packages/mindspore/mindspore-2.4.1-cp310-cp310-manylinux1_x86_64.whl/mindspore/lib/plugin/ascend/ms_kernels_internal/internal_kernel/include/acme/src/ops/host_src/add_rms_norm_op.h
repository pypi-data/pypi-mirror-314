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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ADD_RMS_NORM_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ADD_RMS_NORM_OP_H_

#include <vector>
#include "acme/include/acme_op.h"
#include "acme/include/op_param.h"

namespace mindspore {
namespace acme {
class AddRmsNormOp : public AcmeOp {
 public:
  AddRmsNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
               const NormParam &param, const std::string &op_name)
      : AcmeOp(inputs_ii, outputs_ii, op_name), param_(param) {}
  ~AddRmsNormOp() = default;

  std::string DumpTiling(const RawHostAddr host_ptr) const override;
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  AcmeStatus InitImpl() override;
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;

 private:
  NormParam param_;
};

using AddRmsNormOpPtr = std::shared_ptr<AddRmsNormOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ADD_RMS_NORM_OP_H_