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

#ifndef MS_KERNELS_INTERNAL_HOST_ACME_ROPE_NZ_H_
#define MS_KERNELS_INTERNAL_HOST_ACME_ROPE_NZ_H_

#include "acme/include/acme_op.h"
#include "acme/include/op_param.h"
#include "apply_rotary_pos_emb_op.h"
#include "utils/log/log.h"

namespace mindspore {
namespace acme {
class ApplyRotaryPosEmbNzOp : public ApplyRotaryPosEmbOp {
 public:
  ApplyRotaryPosEmbNzOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                        const ApplyRotaryPosEmbParam &param, const std::string &op_name)
      : ApplyRotaryPosEmbOp(inputs_ii, outputs_ii, param, op_name) {}
  ~ApplyRotaryPosEmbNzOp() = default;

  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream) override;
};

using ApplyRotaryPosEmbNzOpPtr = std::shared_ptr<ApplyRotaryPosEmbNzOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_HOST_ACME_ROPE_NZ_H_
