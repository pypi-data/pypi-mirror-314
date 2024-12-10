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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MATMUL_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MATMUL_OP_H_

#include <algorithm>
#include "acme/include/op_param.h"
#include "acme/src/ops/host_src/multi_impls_op.h"
#include "acme/src/ops/device_src/cce/matmul/matmul.h"
#include "tune_repo/matmul_table.h"
#include "acme/src/ops/device_src/cce/matmul_common/pp_matmul_info.h"
#include "acme/src/ops/device_src/cce/matmul_common/tiling_data.h"
#include "acme/src/ops/device_src/cce/matmul_common/pp_matmul_common_tiling.h"

#include "asdops/op_desc.h"
#include "asdops/operation.h"
#include "asdops/run_info.h"
#include "asdops/tactic.h"
#include "asdops/tensor.h"

#include "backend_param.h"

using namespace mindspore::acme;
using namespace mindspore::acme::tiling;

namespace mindspore {
namespace acme {
enum class MatMulAlgo { PP = 0, LLM_CUSTOM = 1 };
enum class MatMulFusionLevel { NONE = 0, CUBE = 1, MIX = 2 };
enum class MatMulFusionType {
  NONE = 0,
  WITH_RELU = 1,
  WITH_GELU = 2,
  WITH_BIAS = 3,
  WITH_BIAS_FASTGELU = 4
};

class MatmulOp : public MultiImplsOp {
 public:
  MatmulOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
           const MatmulParam &param, const std::string &op_name);
  ~MatmulOp() = default;

  AsdOps::Any BuildAsdParam() override;
  AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape) override;
  const std::string &TargetKernelName() const override { return target_kernel_name; }

  bool IsSupported(const InputDataTypes &dtypes) override { return true; }

  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  AcmeStatus InitImpl() override;
  bool UseAsdopImpl() override;
  AcmeStatus TilingImplAcme(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImplAcme(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                                 const WsAddrList &ws_ptrs, void *stream) override;
  std::string DumpTilingAcme(const RawHostAddr host_ptr) const override;
  uint32_t GetLaunchCoreNumAcme() const override;

 private:
  void SetFusionLevel();
  bool GenTilingId(uint32_t &tiling_id);
  void GetTunedKey();
  void SetTunedValueCustom(const std::vector<int> &tuned_config);
  bool GetPpMatmulTiling(const MatMulInfo &, uint32_t &, PpTilingData &, const REPO &, const std::vector<int> &);
  void TilingBasicFromPp(uint32_t &, PpTilingData &);
  AcmeStatus TilingLLMCustom(RawHostAddr, uint64_t, uint32_t &, const PpTilingData &);
  AcmeStatus TilingPp(RawHostAddr &tiling_addr, uint32_t tiling_id, const uint32_t &block_dim,
                      const PpTilingData &tilingdata);
  AcmeStatus LaunchMix(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, void *stream);

  const std::string target_kernel_name{"MatMulOperation"};
  std::string soc_name_{"UnknownSoc"};
  MatmulParam param_;
  REPO tuning_table_;
  REPO tuning_table_custom_;
  MatMulFusionLevel fusion_level_ = MatMulFusionLevel::NONE;
  std::vector<int> tune_key_;
  MsMatmulTilingData t_;
  uint32_t m_;
  uint32_t n_;
  uint32_t k_;
  MatMulAlgo algo_ = MatMulAlgo::PP;
  internal::HardwareInfo hw_info_;
  bool shuffle_env_{false};
  bool use_asd_impl_{false};
};

using MatmulOpPtr = std::shared_ptr<MatmulOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MATMUL_OP_H_