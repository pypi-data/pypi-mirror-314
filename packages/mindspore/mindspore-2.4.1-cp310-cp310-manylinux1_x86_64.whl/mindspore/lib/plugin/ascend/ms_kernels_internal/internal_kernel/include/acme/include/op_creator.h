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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_OP_CREATOR_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_OP_CREATOR_H_

#include "acme/include/acme_op.h"
#include "acme/include/op_param.h"

namespace mindspore {
namespace acme {
AcmeOpPtr CreateMatmulOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                         const MatmulParam &param, const std::string &op_name);
AcmeOpPtr CreateAddOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                      const std::string &op_name);
AcmeOpPtr CreateAddLayerNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                               const NormParam &param, const std::string &op_name);
AcmeOpPtr CreateAddRmsNormQuantOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                                  const NormParam &param, const std::string &op_name);
AcmeOpPtr CreateCastOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                       const std::string &op_name);
AcmeOpPtr CreateTransposeOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                            const TransposeParam &param, const std::string &op_name);
AcmeOpPtr CreateQuantPerChannelOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                                  const std::string &op_name);
AcmeOpPtr CreateSwishOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                        const std::string &op_name);
AcmeOpPtr CreateSwiGLUOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                         const SwiGLUParam &param, const std::string &op_name);
AcmeOpPtr CreateLogicalNotOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                             const std::string &op_name);
AcmeOpPtr CreateSoftmaxOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                          const SoftmaxParam &param, const std::string &op_name);
AcmeOpPtr CreateReduceSumOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                            const ReduceSumParam &param, const std::string &op_name);
AcmeOpPtr CreateGatherOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                         const GatherParam &param, const std::string &op_name);
AcmeOpPtr CreateApplyRotaryPosEmbOp(const InputsImmutableInfoList &inputs_ii,
                                    const OutputsImmutableInfoList &outputs_ii, const ApplyRotaryPosEmbParam &param,
                                    const std::string &op_name);
AcmeOpPtr CreateApplyRotaryPosEmbNzOp(const InputsImmutableInfoList &inputs_ii,
                                      const OutputsImmutableInfoList &outputs_ii, const ApplyRotaryPosEmbParam &param,
                                      const std::string &op_name);
AcmeOpPtr CreateRmsNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                          const NormParam &param, const std::string &op_name);
AcmeOpPtr CreateMatmulAddRmsNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                                   const MatmulAddRmsNormParam &param, const std::string &op_name);
AcmeOpPtr CreateMultiWeightMatmulOp(const InputsImmutableInfoList &inputs_ii,
                                    const OutputsImmutableInfoList &outputs_ii, const MultiWeightMatmulParam &param,
                                    const std::string &op_name);
// param section 0
AcmeOpPtr CreateGeLUOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                       const std::string &op_name);
AcmeOpPtr CreateAddRmsNormOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                             const NormParam &param, const std::string &op_name);
AcmeOpPtr CreateFlashAttentionScoreOp(const InputsImmutableInfoList &inputs_ii,
                                      const OutputsImmutableInfoList &outputs_ii, const FlashAttentionScoreParam &param,
                                      const std::string &op_name);
AcmeOpPtr CreatePagedAttentionOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                                 const PagedAttentionParam &param, const std::string &op_name);
// param section 1
AcmeOpPtr CreateReshapeAndCacheOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                                  const std::string &op_name);
AcmeOpPtr CreateReshapeAndCacheNzOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                                    const std::string &op_name);
AcmeOpPtr CreateMulOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                      const std::string &op_name);
AcmeOpPtr CreateSubOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                      const std::string &op_name);
AcmeOpPtr CreateRealDivOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                          const std::string &op_name);

// param section 2
AcmeOpPtr CreateFastGeLUOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                           const std::string &op_name);
AcmeOpPtr CreateTransDataOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                            const TransDataParam &param, const std::string &op_name);
AcmeOpPtr CreateQuantLinearSparseOp(const InputsImmutableInfoList &inputs_ii,
                                    const OutputsImmutableInfoList &outputs_ii, const std::string &op_name);
// param section 3

// param section 4

// param section 5

// param section 6

// param section 7

// param section 8

// param section 9

// param section 10

bool IsAcmeKernelDtypesSupported(const std::string op_name, InputDataTypes in_dtypes, InputDataTypes out_dtypes);
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_OP_CREATOR_H_
