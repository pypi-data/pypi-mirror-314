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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_ELEWISE_BINARY_KERNEL_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_ELEWISE_BINARY_KERNEL_H_

void elewise_sub(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                 uint8_t *tiling, int dtype);
void elewise_mul(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                 uint8_t *tiling, int dtype);
void elewise_div(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                 uint8_t *tiling, int dtype);
void elewise_min(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                 uint8_t *tiling, int dtype);
void elewise_max(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                 uint8_t *tiling, int dtype);
void elewise_and(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                 uint8_t *tiling, int dtype);
void elewise_or(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *in1, uint8_t *in2, uint8_t *out,
                uint8_t *tiling, int dtype);

#endif  // MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_ELEWISE_BINARY_KERNEL_H_