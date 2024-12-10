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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_FLASH_ATTENTION_SCORE_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_FLASH_ATTENTION_SCORE_OP_H_

#include "multi_impls_op.h"
#include "acme/src/ops/device_src/cce/flash_attention_score/flash_attention_score_tiling_data.h"

namespace mindspore {
namespace acme {
static std::ostringstream &operator<<(std::ostringstream &os, const BSAttentionTilingData &dt) {
  os << "AcmeFlashAttentionScore Tiling: ";
  os << "\n batch_size:       " << dt.batch_size;
  os << "\n num_heads:        " << dt.num_heads;
  os << "\n max_seqlen:       " << dt.max_seqlen;
  os << "\n head_dim:         " << dt.head_dim;
  os << "\n num_group:        " << dt.num_group;
  os << "\n q_seqlen:         " << dt.q_seqlen;
  os << "\n kv_seqlen:        " << dt.kv_seqlen;
  os << "\n table_block_size: " << dt.table_block_size;
  os << "\n sync_addr:        " << dt.sync_addr;
  os << "\n core_num:         " << dt.core_num;
  os << "\n tor:              " << dt.tor;
  return os;
}

static std::ostringstream &operator<<(std::ostringstream &os, const FlashAttentionScoreParam &dt) {
  os << "AcmeFlashAttentionScore Param: ";
  os << "\n head_num:      " << dt.head_num;
  os << "\n inner_precise: " << dt.inner_precise;
  os << "\n pre_tokens:    " << dt.pre_tokens;
  os << "\n next_tokens:   " << dt.next_tokens;
  os << "\n mask_dtype:    " << dt.mask_dtype;
  os << "\n tor:           " << dt.tor;
  return os;
}

class FlashAttentionScoreOp : public MultiImplsOp {
 public:
  FlashAttentionScoreOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                        const FlashAttentionScoreParam &param, const std::string &op_name);
  ~FlashAttentionScoreOp() = default;

  AsdOps::Any BuildAsdParam() override;
  AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape) override;
  const std::string &TargetKernelName() const override { return target_kernel_name_; }
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  AcmeStatus InitImpl() override;
  bool UseAsdopImpl() override;
  AcmeStatus TilingImplAcme(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImplAcme(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                            const WsAddrList &ws_ptrs, void *stream) override;
  std::string DumpTilingAcme(const RawHostAddr host_ptr) const override;
  uint32_t GetLaunchCoreNumAcme() const override;
  AcmeStatus CreateAsdTensor();
  AcmeStatus UpdateAsdTensor(ShapeInfoList *asd_input_shape, ShapeInfoList *asd_output_shape);
  AcmeStatus UpdateAsdParam();
  AcmeStatus CheckAsdopSupport() const;

 private:
  const std::string target_kernel_name_{"MixOperation"};
  FlashAttentionScoreParam param_;
  InputsDescList asd_inputs_;
  OutputsDescList asd_outputs_;
  uint64_t tiling_key_{0};
  bool has_attn_mask_{false};
  bool has_alibi_mask_{false};
  bool is_910_{false};
  bool is_310p_{false};
};

using FlashAttentionScoreOpPtr = std::shared_ptr<FlashAttentionScoreOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_FLASH_ATTENTION_SCORE_OP_H_