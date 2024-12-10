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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_BINARY_OR_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_BINARY_OR_KERNEL_H_

#include "elewise_binary_base.h"

template <typename T = int16_t>
class OrI16 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline OrI16() { ElewiseBaseWide<T>::SetBinaryFunc(AscendC::Or); }
};

template <typename T = uint16_t>
class OrU16 : public ElewiseBaseWide<T> {
 public:
  __aicore__ inline OrU16() { ElewiseBaseWide<T>::SetBinaryFunc(AscendC::Or); }
};

extern "C" __global__ __aicore__ void or_device_legacy(GM_ADDR x1, GM_ADDR x2, GM_ADDR y, GM_ADDR tiling, int32_t dtype) {
  if (dtype == 6) {  // int16
    OrI16<int16_t> op;
    op.InitBinary(x1, x2, y, tiling);
    op.ProcessBinary();
  } else if (dtype == 7) {  // uint16
    OrU16<uint16_t> op;
    op.InitBinary(x1, x2, y, tiling);
    op.ProcessBinary();
  }
}

#endif  // MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_BINARY_OR_KERNEL_H_
