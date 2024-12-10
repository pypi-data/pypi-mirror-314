/**
 * Copyright 2023-2024 Huawei Technologies Co., Ltd
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
#ifndef ATTENTION_PARAMS_H
#define ATTENTION_PARAMS_H

#include "op_param.h"

namespace mindspore {
namespace internal {
struct FlashAttentionScoreParam : public OpParam {
  int head_num = 0;
  int inner_precise = 0;
  int pre_tokens = 2147483647;
  int next_tokens = 0;
  int sparse_mode = 0;
  int32_t mask_dtype_ = 0;
  DIMS mask_dims_;

  bool CanSupportAsd();
};

struct PagedAttentionParam : public OpParam {
  int inner_precise = 0;
};
}  // namespace internal
}  // namespace mindspore
#endif
