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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_RELU_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_RELU_KERNEL_H_

#include "elewise_unary_base.h"

template <typename T = float>
class ReluFp32 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline ReluFp32() { ElewiseBaseWide<T>::SetUnaryFunc(AscendC::Relu); }
};

template <typename T = half>
class ReluFp16 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline ReluFp16() { ElewiseBaseWide<T>::SetUnaryFunc(AscendC::Relu); }
};

template <typename T = int32_t>
class ReluI32 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline ReluI32() { ElewiseBaseWide<T>::SetUnaryFunc(AscendC::Relu); }
};

extern "C" __global__ __aicore__ void relu_device_legacy(GM_ADDR x, GM_ADDR y, GM_ADDR tiling, int32_t dtype) {
  if (dtype == 1) {  // fp16
    ReluFp16<half> op;
    op.InitUnary(x, y, tiling);
    op.ProcessUnary();
  } else if (dtype == 0) {  // fp32
    ReluFp32<float> op;
    op.InitUnary(x, y, tiling);
    op.ProcessUnary();
  } else if (dtype == 3) {  // int32
    ReluI32<int32_t> op;
    op.InitUnary(x, y, tiling);
    op.ProcessUnary();
  }
}
#endif  // MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_RELU_KERNEL_H_