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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_RECIPROCAL_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_RECIPROCAL_KERNEL_H_

#include "elewise_unary_base.h"

template <typename T = float>
class ReciprocalFp32 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline ReciprocalFp32() { ElewiseBaseWide<T>::SetUnaryFunc(AscendC::Reciprocal); }
};

template <typename T = half>
class ReciprocalFp16 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline ReciprocalFp16() { ElewiseBaseWide<T>::SetUnaryFunc(AscendC::Reciprocal); }
};

extern "C" __global__ __aicore__ void reciprocal_device_legacy(GM_ADDR x1, GM_ADDR y, GM_ADDR tiling, int32_t dtype) {
  if (dtype == 1) {  // fp16
    ReciprocalFp16<half> op;
    op.InitUnary(x1, y, tiling);
    op.ProcessUnary();
  } else if (dtype == 0) {  // fp32
    ReciprocalFp32<float> op;
    op.InitUnary(x1, y, tiling);
    op.ProcessUnary();
  }
}
#endif  // MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_RECIPROCAL_KERNEL_H_