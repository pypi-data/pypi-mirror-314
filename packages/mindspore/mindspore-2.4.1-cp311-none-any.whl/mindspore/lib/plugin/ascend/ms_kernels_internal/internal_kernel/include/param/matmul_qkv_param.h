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
#ifndef MATMUL_QKV_PARAMS_H_
#define MATMUL_QKV_PARAMS_H_

#include "ms_int_types.h"
#include "op_param.h"

namespace mindspore {
namespace internal {
struct MatmulQkvParam : public OpParam {
  uint32_t n0_len{0};
  uint32_t n1_len{0};
  uint32_t n2_len{0};
  bool transposeA;
  bool transposeB;
  MatmulQkvParam() : transposeA(false), transposeB(true) {}
  MatmulQkvParam(uint32_t n0, uint32_t n1, uint32_t n2, bool tA, bool tB)
      : n0_len(n0), n1_len(n1), n2_len(n2), transposeA(tA), transposeB(tB) {}
  bool operator==(const MatmulQkvParam &other) const {
    return (this->n0_len == other.n0_len && this->n1_len == other.n1_len && this->n2_len == other.n2_len &&
            this->transposeA == other.transposeA && this->transposeB == other.transposeB);
  }
  int32_t silu_position{-1};
  bool with_bias{false};
};
}  // namespace internal
}  // namespace mindspore
#endif
