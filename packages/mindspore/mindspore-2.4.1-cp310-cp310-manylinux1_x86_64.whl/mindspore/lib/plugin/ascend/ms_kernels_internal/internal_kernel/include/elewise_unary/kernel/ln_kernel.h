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
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either Lnress or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_LN_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_LN_KERNEL_H_

#include "elewise_unary_base.h"

template <typename T = float>
class LnFp32 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline LnFp32() { ElewiseBaseWide<T>::SetUnaryFunc(AscendC::Ln); }
};

template <typename T = half>
class LnFp16 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline LnFp16() { ElewiseBaseWide<T>::SetUnaryFunc(AscendC::Ln); }
};

extern "C" __global__ __aicore__ void ln_device_legacy(GM_ADDR x, GM_ADDR y, GM_ADDR tiling, int32_t dtype) {
  if (dtype == 1) {  // fp16
    LnFp16<half> op;
    op.InitUnary(x, y, tiling);
    op.ProcessUnary();
  } else if (dtype == 0) {  // fp32
    LnFp32<float> op;
    op.InitUnary(x, y, tiling);
    op.ProcessUnary();
  }
}
#endif  // MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_UNARY_LN_KERNEL_H_