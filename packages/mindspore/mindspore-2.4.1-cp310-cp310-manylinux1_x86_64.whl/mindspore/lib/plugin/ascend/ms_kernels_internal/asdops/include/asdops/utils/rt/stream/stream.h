/*
 * Copyright (c) 2024 Huawei Technologies Co., Ltd.
 * AscendOpCommonLib is licensed under Mulan PSL v2.
 * You can use this software according to the terms and conditions of the Mulan PSL v2.
 * You may obtain a copy of Mulan PSL v2 at:
 *          http://license.coscl.org.cn/MulanPSL2
 * THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
 * EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
 * MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
 * See the Mulan PSL v2 for more details.
 */
#ifndef COMMON_RT_STREAM_STREAM_H
#define COMMON_RT_STREAM_STREAM_H
#include "asdops/utils/rt/base/types.h"

#ifdef __cplusplus
extern "C" {
#endif
namespace AsdOps {
int AsdRtStreamCreate(AsdRtStream *stream, int32_t priority = 0);
int AsdRtStreamDestroy(AsdRtStream stream);
int AsdRtStreamSynchronize(AsdRtStream stream);
int AsdRtStreamGetId(AsdRtStream stream, int32_t *streamId);
}
#ifdef __cplusplus
}
#endif
#endif