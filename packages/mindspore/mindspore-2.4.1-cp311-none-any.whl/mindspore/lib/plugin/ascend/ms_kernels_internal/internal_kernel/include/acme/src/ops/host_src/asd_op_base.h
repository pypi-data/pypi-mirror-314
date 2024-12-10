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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_OPS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_OPS_H_

#include <any>
#include "acme/include/acme_op.h"

#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"

namespace mindspore {
namespace acme {
class HostRunInfoAsd : public HostRunInfo {
 public:
  HostRunInfoAsd() = default;
  ~HostRunInfoAsd() = default;

  HostRunInfoAsd(const HostRunInfoAsd &other);
  HostRunInfoAsd(HostRunInfoAsd &other);

  const HostRunInfoAsd &operator=(const HostRunInfoAsd &other);
  const HostRunInfoAsd &operator=(HostRunInfoAsd &other);
  AsdOps::RunInfo run_info_;
};
using HostRunInfoAsdPtr = std::shared_ptr<HostRunInfoAsd>;

class AsdOp : public AcmeOp {
 public:
  AsdOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
        const std::string &op_name, const AsdOps::Any &param, const std::string &asd_op_name);
  AsdOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
        const std::string &op_name, const std::string &asd_op_name);
  virtual ~AsdOp() = default;
  AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape) override;
  void SetTilingInfo(const TilingInfoPtr &tiling_info) override;

  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;

  std::string DumpTiling(const RawHostAddr host_ptr) const override;
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;
  uint32_t GetLaunchCoreNum() const override;
  std::string GetOpName() override { return tactic_name_; };
  AsdOps::Any GetParam();
  void UpdateLaunchParam(const AsdOps::Any &param);

 protected:
  virtual void UpdateLaunchParam();
  AcmeStatus InitImpl() override;
  void SetParam(const AsdOps::Any &param);
  AcmeStatus SetTactic();
  AsdOps::Operation *GetOP() const { return op_; };
  AsdOps::LaunchParam launch_param_;

 private:
  void UpdateRunInfo(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                     void *stream);

  uint32_t dim_axis_{0};
  bool is_same_shape_{true};
  ShapeInfo input_shape1_;
  ShapeInfo input_shape2_;
  AsdOps::Any asd_param_;
  std::string asd_op_name_;
  std::string tactic_name_{"UnknownTactic"};
  AsdOps::OpDesc op_desc_;
  AsdOps::Tactic *tactic_{nullptr};
  AsdOps::Operation *op_{nullptr};
  HostRunInfoAsdPtr host_run_info_asd_ptr_{nullptr};
  std::vector<size_t> inputs_type_size_;
  std::vector<size_t> outputs_type_size_;
};

using AsdOpPtr = std::shared_ptr<AsdOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_OPS_H_