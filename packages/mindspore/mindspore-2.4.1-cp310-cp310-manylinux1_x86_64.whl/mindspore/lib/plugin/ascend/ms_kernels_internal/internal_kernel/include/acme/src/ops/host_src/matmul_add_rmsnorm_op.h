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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MATMUL_ADD_RMSNORM_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_MATMUL_ADD_RMSNORM_OP_H_

#include "acme/include/op_param.h"
#include "acme/include/acme_op.h"
#include "acme/src/ops/device_src/cce/matmul_add_rmsnorm/matmul_add_rmsnorm_tiling.h"

#include "acme/src/ops/device_src/cce/matmul_common/pp_matmul_common_tiling.h"
#include "tune_repo/utils.h"
#include "backend_param.h"

using namespace mindspore::acme;
using namespace mindspore::acme::tiling;

namespace mindspore {
namespace acme {

class MatmulAddRmsNormOp : public AcmeOp {
 public:
  MatmulAddRmsNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                     const MatmulAddRmsNormParam &param, const std::string &op_name)
      : AcmeOp(inputs_ii, outputs_ii, op_name), param_(param) {}
  ~MatmulAddRmsNormOp() = default;

  std::string DumpTiling(const RawHostAddr host_ptr) const override;

  bool IsSupported(const InputDataTypes &dtypes) override { return true; }

  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  AcmeStatus InitImpl() override;
  AcmeStatus TilingImpl(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                        const WsAddrList &ws_ptrs, void *stream) override;

 private:
  MatmulAddRmsNormParam param_;
  REPO tuningTable_;
  REPO tuningTableCustom_;
  internal::HardwareInfo hw_info_;
  uint32_t m_, k_, n_;
  bool trans_a_{false};
  bool trans_b_{true};
  std::vector<int> tune_key_;
  DataType MatMulIn_dtype_;
  DataType RmsNorm_dtype_;
  uint32_t dtype_key = 0;
  int block_dim_ = 0;
  void *ffts_addr;
  void GetTunedKey();
  void TilingBasicFromPp(uint32_t &blockDim, PpTilingData &tilingdata);
};

}  // namespace acme
}  // namespace mindspore
#endif
