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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_PAGED_ATTENTION_OP_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_PAGED_ATTENTION_OP_H_

#include "multi_impls_op.h"
#include "acme/src/ops/device_src/cce/paged_attention/paged_attention_tiling_data.h"

namespace mindspore {
namespace acme {
static std::ostringstream &operator<<(std::ostringstream &os, const PagedAttentionParam &dt) {
  os << "AcmePagedAttention Param: ";
  os << "\n inner_precise:  " << dt.inner_precise;
  os << "\n head_num:       " << dt.head_num;
  os << "\n kv_head_num:    " << dt.kv_head_num;
  os << "\n tor:            " << dt.tor;
  os << "\n kv_seq_len:     ";
  os << "[";
  for (auto element : dt.kv_seq_len) {
    os << element << " ";
  }
  os << "]";
  os << "\n q_seq_len:      ";
  os << "[";
  for (auto element : dt.kv_seq_len) {
    os << element << " ";
  }
  os << "]";
  return os;
}

class PagedAttentionOp : public MultiImplsOp {
 public:
  PagedAttentionOp(const InputsImmutableInfoList &inputs_ii, const OutputsImmutableInfoList &outputs_ii,
                   const PagedAttentionParam &param, const std::string &op_name);
  virtual ~PagedAttentionOp() = default;

  AsdOps::Any BuildAsdParam() override;
  AcmeStatus UpdateShape(const ShapeInfoList &inputs_shape, const ShapeInfoList &outputs_shape) override;
  AcmeStatus UpdateParam(const void *) override;
  const std::string &TargetKernelName() const override { return target_kernel_name_; }
  ShapeInfoList InferShape(const ShapeInfoList &inputs_shape) const override;

 protected:
  AcmeStatus InitImpl() override;
  bool UseAsdopImpl() override;
  AcmeStatus LaunchImpl(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs, const WsAddrList &ws_ptrs,
                        void *stream);
  AcmeStatus TilingImplAcme(RawHostAddr host_ptr, HostRunInfoPtr *run_info_ptr) override;
  AcmeStatus LaunchImplAcme(const InputsAddrList &input_ptrs, const OutputsAddrList &output_ptrs,
                            const WsAddrList &ws_ptrs, void *stream) override;
  std::string DumpTilingAcme(const RawHostAddr host_ptr) const override;
  uint32_t GetLaunchCoreNumAcme() const override;
  AcmeStatus CreateAsdTensor();
  AcmeStatus UpdateAsdParam();
  AcmeStatus UpdateAsdTensor();
  AcmeStatus CheckAsdopSupport() const;

 private:
  const std::string target_kernel_name_{"MixOperation"};
  PagedAttentionParam param_;
  InputsDescList asd_inputs_;
  OutputsDescList asd_outputs_;
  InputsImmutableInfoList asd_inputs_ii_;
  InputsImmutableInfoList asd_outputs_ii_;
  ShapeInfoList asd_input_shape_;
  ShapeInfoList asd_output_shape_;
  uint64_t tiling_key_{0};
  bool is_custom_quant_{false};
  bool has_mask_{false};
  bool has_alibi_mask_{false};
  bool has_attn_mask_{false};
  int alibi_mask_index_{-1};
  int attn_mask_index_{-1};
  bool is_910_{false};
  bool is_310p_{false};
  bool is_asd_quant_{false};
  int dequant_shape_{0};
};

using PagedAttentionOpPtr = std::shared_ptr<PagedAttentionOp>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_OPS_HOST_SRC_PAGED_ATTENTION_OP_H_
