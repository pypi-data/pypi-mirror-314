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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MULTI_WEIGHT_MATMUL_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MULTI_WEIGHT_MATMUL_OP_H_

#include <algorithm>
#include "acme/include/acme_op.h"
#include "acme/include/op_param.h"
#include "acme/src/ops/device_src/cce/multi_weight_matmul/multi_weight_matmul_kernel.h"
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
enum class MultiMatMulAlgo { PP = 0, LLM_CUSTOM = 1 };
enum class MultiMatMulFusionLevel { NONE = 0, CUBE = 1, MIX = 2 };
enum class MultiMatMulFusionType { NONE = 0, WITH_BIAS = 1, WITH_SILU = 2 };

class MultiWeightMatmulOp : public AcmeOp {
 public:
  MultiWeightMatmulOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                      const MultiWeightMatmulParam &param, const std::string &op_name);
  ~MultiWeightMatmulOp() = default;

  std::string DumpTiling(const RawHostAddr host_ptr) const override;

  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  AcmeStatus InitImpl() override;
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;

 private:
  bool GenTilingId(uint32_t &tiling_id);
  void GetTunedKey();
  uint32_t MixSwizzle(acme::tiling::PpTilingData *tilingdata);
  bool GetPpMatmulTiling(const acme::tiling::MatMulInfo &, uint32_t &, acme::tiling::PpTilingData &);
  void TilingBasicFromPp(uint32_t &, acme::tiling::PpTilingData &);
  AcmeStatus TilingLLMCustom(RawHostAddr, uint64_t, uint32_t &, const acme::tiling::PpTilingData &);
  AcmeStatus TilingPp(RawHostAddr &tiling_addr, uint32_t tiling_id, const uint32_t &block_dim,
                      const acme::tiling::PpTilingData &tilingdata);
  AcmeStatus LaunchMix(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, void *stream);

  MultiWeightMatmulParam param_;
  REPO tuning_table_;
  std::vector<int> tune_key_;
  MultiMatMulFusionLevel fusion_level_ = MultiMatMulFusionLevel::NONE;
  MultiMatMulAlgo algo_ = MultiMatMulAlgo::PP;
  internal::HardwareInfo hw_info_;
  uint32_t m_;
  uint32_t k_;
  uint32_t n0_;
  uint32_t n1_;
  uint32_t n2_;
  uint32_t fusion_type_{0};
  int32_t silu_position_{-1};
};

}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MULTI_WEIGHT_MATMUL_OP_H_