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
#ifndef MATMUL_EXT_PARAMS_H_
#define MATMUL_EXT_PARAMS_H_

#include "ms_int_types.h"
#include "op_param.h"

namespace mindspore {
namespace internal {

struct MatMulExtParam : public OpParam {
  int input_dtype = -1;
  int weight_dtype = -1;
  int bias_dtype = -1;
  int output_dtype = -1;
  bool with_relu = false;
  bool with_gelu = false;
  bool with_bias = false;
  bool with_bias_fastgelu = false;
};

}  // namespace internal
}  // namespace mindspore
#endif
