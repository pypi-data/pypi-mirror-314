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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ROPE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ROPE_H_

void apply_rotary_pos_emb_do(uint32_t blockDim, void *l2ctrl, void *stream, uint8_t *query, uint8_t *key, uint8_t *cos,
                             uint8_t *sin, uint8_t *position_id, uint8_t *query_embed, uint8_t *key_embed,
                             uint8_t *workspace, uint8_t *tiling);
#endif
