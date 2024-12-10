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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ADDLAYERNORM_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ADDLAYERNORM_OP_H_

#include "acme/include/acme_op.h"
#include "acme/include/op_param.h"
#include "acme/src/ops/device_src/ascendc/add_layer_norm/add_layer_norm_tiling.h"

namespace mindspore {
namespace acme {
static constexpr int RESERVED_WORKSPACE_SIZE_910B = 16 * 1024 * 1024;
static constexpr int RESERVED_WORKSPACE_SIZE_310P = 2 * 1024 * 1024;

class AddLayerNormOp : public AcmeOp {
 public:
  AddLayerNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                 const NormParam &param, const std::string &op_name)
      : AcmeOp(inputs_ii, outputs_ii, op_name), param_(param){};
  ~AddLayerNormOp() = default;

  std::string DumpTiling(const RawHostAddr host_ptr) const override;
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;
  std::vector<size_t> GetWorkspaceSize() const override {
    size_t sysWorkspaceSize = RESERVED_WORKSPACE_SIZE_910B;
    if ((soc_.find("Ascend310P") != std::string::npos)) {
      sysWorkspaceSize = RESERVED_WORKSPACE_SIZE_310P;
    }
    return {1 + sysWorkspaceSize};
  };

 protected:
  AcmeStatus InitImpl() override;
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;

 private:
  NormParam param_;
};

using AddLayerNormOpPtr = std::shared_ptr<AddLayerNormOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ADDLAYERNORM_OP_H_