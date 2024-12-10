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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ROPE_NZ_TILING_DATA_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ROPE_NZ_TILING_DATA_H_

#include <stdint.h>

struct RopeTilingNzData {
  uint32_t hiddenSizeQ{16};
  uint32_t hiddenSizeK{16};
  uint32_t headDim{1};  // qk头长度的最大值
  uint32_t headNumQ{1};
  uint32_t headNumK{1};
  uint32_t rotaryCoeff{4};  // 旋转系数
  uint32_t ntokens{1};      // 总token数
  uint32_t realCore{0};     // 实际用到核数
  uint32_t cosFormat{0};    // 是否复用cos sin
  uint32_t batch{32};       // 几个batch
  uint32_t maxUbSize{0};    // 最大UB内存
  uint32_t tilingId{0};

  uint32_t seqLen;
  uint32_t broadCastCos{0};
  uint32_t posDtype;
  uint32_t posSize;
  uint32_t maxSeqLen;
};

#endif
