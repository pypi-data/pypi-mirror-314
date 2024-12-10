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

#ifndef MS_KERNELS_INTERNAL_SRC_UTILS_UTILS_H_
#define MS_KERNELS_INTERNAL_SRC_UTILS_UTILS_H_

#include <iostream>
#include <map>
#include <set>
#include "include/op_param.h"

namespace mindspore::internal {
inline void SplitString(const std::string &str, char delim, std::set<std::string> &output_list) {
  std::stringstream ss(str);
  std::string item;
  std::vector<std::string> elems;
  while (std::getline(ss, item, delim)) {
    if (!item.empty()) {
      output_list.emplace(item);
    }
  }
}

template <typename T>
static std::ostream &operator<<(std::ostream &os, const std::vector<T> &v) {
  os << "[size " << v.size() << "]";
  os << "[data";
  for (size_t i = 0; i < v.size(); i++) {
    os << " " << v[i];
  }
  os << "]";
  return os;
}

inline std::string OpIdToString(int id) {
  std::map<int, std::string> op_id_string = {
    {OpId::MatMul, "MatMul"},
    {OpId::ReshapeAndCache, "ReshapeAndCache"},
    {OpId::Slice, "Slice"},
    {OpId::Gather, "Gather"},
    {OpId::ApplyRotaryPosEmb, "ApplyRotaryPosEmb"},
    {OpId::Add, "Add"},
    {OpId::Sub, "Sub"},
    {OpId::Exp, "Exp"},
    {OpId::FlashAttentionScore, "FlashAttentionScore"},
    {OpId::PagedAttention, "PagedAttention"},
    {OpId::Cast, "Cast"},
    {OpId::Gelu, "Gelu"},
    {OpId::Transpose, "Transpose"},
    {OpId::Equal, "Equal"},
    {OpId::NotEqual, "NotEqual"},
    {OpId::LogicalNot, "LogicalNot"},
    {OpId::Less, "Less"},
    {OpId::LessEqual, "LessEqual"},
    {OpId::Greater, "Greater"},
    {OpId::GreaterEqual, "GreaterEqual"},
    {OpId::Mul, "Mul"},
    {OpId::RealDiv, "RealDiv"},
    {OpId::LayerNorm, "LayerNorm"},
    {OpId::AddLayerNorm, "AddLayerNorm"},
    {OpId::RmsNorm, "RmsNorm"},
    {OpId::AddRmsNorm, "AddRmsNorm"},
    {OpId::RmsNormQuant, "RmsNormQuant"},
    {OpId::AddRmsNormQuant, "AddRmsNormQuantV2"},
    {OpId::Softmax, "Softmax"},
    {OpId::Split, "Split"},
    {OpId::Swish, "Swish"},
    {OpId::SwiGLU, "SwiGLU"},
    {OpId::Concat, "Concat"},
    {OpId::MatmulQkv, "MatmulQkv"},
    {OpId::MaskedFill, "MaskedFill"},
    {OpId::BroadcastTo, "BroadcastTo"},
    {OpId::ReduceSum, "ReduceSum"},
    {OpId::TopK, "TopK"},
    {OpId::Tile, "Tile"},
    {OpId::FastGeLU, "FastGeLU"},
    {OpId::TransData, "TransData"},
    {OpId::ReshapeAndCacheNz, "ReshapeAndCache"},
    {OpId::ApplyRotaryPosEmbNz, "ApplyRotaryPosEmb"},
    {OpId::QuantPerChannel, "QuantV2"},
    {OpId::QuantLinearSparse, "QuantLinearSparse"},
  };

  auto iter = op_id_string.find(id);
  if (iter != op_id_string.end()) {
    return iter->second;
  }

  std::string err_info = "Op not defined! index: " + std::to_string(id);
  return err_info;
}
}  // namespace mindspore::internal
#endif  //    MS_KERNELS_INTERNAL_SRC_UTILS_UTILS_H_
