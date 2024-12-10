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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_OP_PARAM_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_OP_PARAM_H_

#include <stdint.h>
#include <vector>

namespace mindspore {
namespace acme {
// matmul fused op
constexpr auto kAcmeMatMulOpName = "MatMul";
constexpr auto kAcmeMultiWeightMatmulOpName = "MultiWeightMatmul";
constexpr auto kAcmeMatMulAddRmsNormOpName = "MatMulAddRmsNorm";
// attention fused op
constexpr auto kAcmeFlashAttentionScoreOpName = "FlashAttentionScore";
constexpr auto kAcmePagedAttentionOpName = "PagedAttention";
constexpr auto kAcmeReshapeAndCacheOpName = "ReshapeAndCache";
constexpr auto kAcmeReshapeAndCacheNzOpName = "ReshapeAndCacheNz";
constexpr auto kAcmeApplyRotaryPosEmbOpName = "ApplyRotaryPosEmb";
constexpr auto kAcmeApplyRotaryPosEmbNzOpName = "ApplyRotaryPosEmbNz";
// norm fused op
constexpr auto kAcmeAddLayerNormOpName = "AddLayerNorm";
constexpr auto kAcmeRmsNormOpName = "RmsNorm";
constexpr auto kAcmeAddRmsNormOpName = "AddRmsNorm";
constexpr auto kAcmeRmsNormQuantOpName = "RmsNormQuant";
constexpr auto kAcmeAddRmsNormQuantOpName = "AddRmsNormQuantV2";
// activation
constexpr auto kAcmeReluOpName = "Relu";
constexpr auto kAcmeGeLUOpName = "GeLU";
constexpr auto kAcmeFastGeLUOpName = "FastGeLU";
constexpr auto kAcmeSwishOpName = "Swish";
constexpr auto kAcmeSwiGLUOpName = "SwiGLU";
// elewise unary
constexpr auto kAcmeCastOpName = "Cast";
constexpr auto kAcmeExpOpName = "Exp";
constexpr auto kAcmeLnOpName = "Ln";
constexpr auto kAcmeRsqrtOpName = "Rsqrt";
constexpr auto kAcmeSqrtOpName = "Sqrt";
constexpr auto kAcmeAbsOpName = "Abs";
constexpr auto kAcmeReciprocalOpName = "Reciprocal";
// elewise binary
constexpr auto kAcmeAddOpName = "Add";
constexpr auto kAcmeSubOpName = "Sub";
constexpr auto kAcmeMulOpName = "Mul";
constexpr auto kAcmeDivOpName = "Div";
constexpr auto kAcmeRealDivOpName = "RealDiv";
constexpr auto kAcmeMaxOpName = "Max";
constexpr auto kAcmeMinOpName = "Min";
constexpr auto kAcmeNotOpName = "Not";
constexpr auto kAcmeOrOpName = "Or";
constexpr auto kAcmeAndOpName = "And";
constexpr auto kAcmeEqualOpName = "Equal";
constexpr auto kAcmeNotEqualOpName = "NotEqual";
constexpr auto kAcmeLessOpName = "Less";
constexpr auto kAcmeLessEqualOpName = "LessEqual";
constexpr auto kAcmeGreaterOpName = "Greater";
constexpr auto kAcmeGreaterEqualOpName = "GreaterEqual";
constexpr auto kAcmeLogicalNotOpName = "LogicalNot";
// others
constexpr auto kAcmeGatherOpName = "Gather";
constexpr auto kAcmeTransposeOpName = "Transpose";
constexpr auto kAcmeTransDataOpName = "TransData";
constexpr auto kAcmeQuantPerChannelOpName = "QuantPerChannel";
constexpr auto kAcmeSoftmaxOpName = "Softmax";
constexpr auto kAcmeReduceSumOpName = "ReduceSum";
constexpr auto kAcmeQuantLinearSparseOpName = "QuantLinearSparse";

struct AxesParam {
  std::vector<int64_t> axes;
};

using TransposeParam = AxesParam;
using SoftmaxParam = AxesParam;
using ReduceSumParam = AxesParam;

struct GatherParam {
  int64_t batch_dims;
  std::vector<int64_t> axes;
};

struct SwiGLUParam {
  int64_t axis;
};

struct MatmulParam {
  bool transpose_a{false};
  bool transpose_b{false};
  bool enable_dequant{false};
  bool with_relu{false};
  bool with_gelu{false};
  bool with_bias{false};
  bool with_bias_fastgelu{false};
  bool enable_shuffle{false};
};

struct MatmulAddRmsNormParam {
  bool transpose_a{false};
  bool transpose_b{false};
  float eps{1e-6};
};

struct MultiWeightMatmulParam {
  uint32_t n0_len{0};
  uint32_t n1_len{0};
  uint32_t n2_len{0};
  bool transpose_a;
  bool transpose_b;
  int32_t silu_position{-1};
  bool with_bias{false};
};

struct NormParam {
  float eps;
  bool operator==(const NormParam &other) const { return this->eps == other.eps; }
};

struct ApplyRotaryPosEmbParam {
  // cos_format=0  shape是[maxSeqLen, headDim]，    cos/sin不交替
  // cos_format=1  shape是[maxSeqLen, headDim]，    cos/sin交替
  // cos_format=2  shape是[batch*seqLen, headDim]， cos/sin不交替
  // cos_format=3  shape是[batch*seqLen, headDim]， cos/sin交替
  int32_t cos_format{0};
  int32_t rotary_coeff{-1};
  std::vector<int32_t> batch_valid_length;
};

struct TransDataParam {
  enum TransdataType { UNDEFINED = 0, FRACTAL_NZ_TO_ND, ND_TO_FRACTAL_NZ };
  TransdataType transdataType = UNDEFINED;
  enum SpecialType { NORMAL = 0, ATTENTION_INPUT_QKV, ATTENTION_INPUT_MASK };
  int64_t specialTransdata = NORMAL;
};

struct FlashAttentionScoreParam {
  int32_t head_num = 0;
  int32_t inner_precise = 0;
  int32_t pre_tokens = 2147483647;
  int32_t next_tokens = 0;
  int32_t sparse_mode = 0;
  int32_t mask_dtype = 0;
  int32_t input_layout = 0;
  std::vector<int64_t> mask_dims;
  std::vector<int32_t> kv_seq_len;
  std::vector<int32_t> q_seq_len;
  float tor = 0;

  enum InputLayoutMode : int64_t { 
    BSH = 0,
    BNSD = 1,
    SBH = 2,
    BSND = 3,
    TND = 4,
    TH = 5,
    NSD = 6,
    SH = 7
  };
};

struct PagedAttentionParam {
  int32_t inner_precise = 0;
  int32_t head_num = 0;
  int32_t kv_head_num = 0;
  std::vector<int32_t> kv_seq_len;
  std::vector<int32_t> q_seq_len;
  float tor = 0;

  enum MaskType : uint32_t {
      kMaskTypeNone = 0,
      kMaskTypeAlibi = 1,
      kMaskTypeLookAhead = 2
  };
  MaskType mask_type = kMaskTypeNone;
  int32_t kv_cache_quant_mode = 0;
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_OP_PARAM_H_
