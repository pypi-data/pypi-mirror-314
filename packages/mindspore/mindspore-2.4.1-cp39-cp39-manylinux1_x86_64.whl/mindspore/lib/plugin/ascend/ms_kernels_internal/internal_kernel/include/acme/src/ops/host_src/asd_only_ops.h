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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_ONLY_OPS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_ONLY_OPS_H_

#include "acme/include/op_param.h"
#include "acme/src/ops/host_src/asd_op_base.h"
#include "acme/src/ops/host_src/asd_elewise_op.h"
#include "acme/src/utils/asd_utils.h"

#define DECLARE_ASD_OPS_WITH_PARAM(op_name, PARAM_NAME, PARENT)                                        \
  class op_name##Op : public PARENT {                                                                  \
   public:                                                                                             \
    op_name##Op(const InputsImmutableInfoList &, const OutputsImmutableInfoList &, const PARAM_NAME &, \
                const std::string &);                                                                  \
    ~op_name##Op() = default;                                                                          \
  };                                                                                                   \
  using op_name##OpPtr = std::shared_ptr<op_name##Op>;

#define DECLARE_ASD_OPS_NO_PARAM(op_name, PARENT)                                                        \
  class op_name##Op : public PARENT {                                                                    \
   public:                                                                                               \
    op_name##Op(const InputsImmutableInfoList &, const OutputsImmutableInfoList &, const std::string &); \
    ~op_name##Op() = default;                                                                            \
  };                                                                                                     \
  using op_name##OpPtr = std::shared_ptr<op_name##Op>;

namespace mindspore {
namespace acme {
DECLARE_ASD_OPS_WITH_PARAM(Transpose, TransposeParam, AsdOp)

DECLARE_ASD_OPS_NO_PARAM(Swish, AsdOp)
DECLARE_ASD_OPS_WITH_PARAM(SwiGLU, SwiGLUParam, AsdOp)
DECLARE_ASD_OPS_NO_PARAM(LogicalNot, AsdElewiseOp)
DECLARE_ASD_OPS_NO_PARAM(Add, AsdElewiseOp)
DECLARE_ASD_OPS_NO_PARAM(Mul, AsdElewiseOp)
DECLARE_ASD_OPS_NO_PARAM(RealDiv, AsdElewiseOp)
DECLARE_ASD_OPS_NO_PARAM(Sub, AsdElewiseOp)
DECLARE_ASD_OPS_NO_PARAM(QuantPerChannel, AsdElewiseOp)
DECLARE_ASD_OPS_NO_PARAM(FastGeLU, AsdOp)

DECLARE_ASD_OPS_WITH_PARAM(Softmax, SoftmaxParam, AsdOp)
DECLARE_ASD_OPS_WITH_PARAM(ReduceSum, ReduceSumParam, AsdOp)
DECLARE_ASD_OPS_WITH_PARAM(Gather, GatherParam, AsdOp)

class QuantLinearSparseOp : public AsdOp {
 public:
  QuantLinearSparseOp(const InputsImmutableInfoList &, const OutputsImmutableInfoList &, const std::string &);
  ~QuantLinearSparseOp() = default;

 protected:
  AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape) override;
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;
  void UpdateDeqScale(const ShapeInfoList &inputs_shape);

 private:
  bool is_310p_{false};
};
using QuantLinearSparseOpPtr = std::shared_ptr<QuantLinearSparseOp>;

class TransDataOp : public AsdOp {
 public:
  TransDataOp(const InputsImmutableInfoList &, const OutputsImmutableInfoList &, const TransDataParam &,
              const std::string &);
  ~TransDataOp() = default;

 protected:
  void UpdateLaunchParam() override;
  void Process310TensorDims(AsdOps::Tensor &tensor, const DIMS &dims, const DataType &dtype,
                            const TensorFormat &format);

 private:
  TransDataParam param_;
  bool is_310p_{false};
};
using TransDataOpPtr = std::shared_ptr<TransDataOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_ASD_ONLY_OPS_H_
