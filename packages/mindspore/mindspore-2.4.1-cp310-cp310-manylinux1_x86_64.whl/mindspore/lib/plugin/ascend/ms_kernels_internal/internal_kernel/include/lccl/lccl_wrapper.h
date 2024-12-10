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
#ifndef LCCL_WRAPPER_H_
#define LCCL_WRAPPER_H_

#include <memory>
#include "lccl.h"

#ifdef __cplusplus
extern "C" {
#endif

using namespace Lcal;
using LcclComm = std::shared_ptr<Lccl>;
enum class LcclResult {
    LCAL_SUCCESS = 0,
    LCAL_ERROR_NOT_INITIALIZED = -1,
    LCAL_ERROR_ASDRT = -2,
    LCAL_ERROR_PARA_CHECK_FAIL = -3,
    LCAL_ERROR_INTERNAL = -4,
    LCAL_ERROR_TIMEOUT = -5,
    LCCL_ERROR_INIT_HCCL_FAILED = -6
};

extern LcclResult LcclCommInitRank(uint32_t nRanks, uint32_t rank, LcclComm *comm);

extern LcclResult LcclAllReduce(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType,
                                HcclReduceOp op, aclrtStream stream);

extern LcclResult LcclReduceScatter(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType,
                                    HcclReduceOp op, aclrtStream stream);

extern LcclResult LcclAllGather(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType, aclrtStream stream);

extern LcclResult LcclAll2All(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType, aclrtStream stream);

extern LcclResult LcclBroadcast(void *buff, int64_t count, HcclDataType dataType, int32_t root, aclrtStream stream);

extern LcclResult LcclCommDestroy(LcclComm comm);

#ifdef __cplusplus
}
#endif

#endif  // LCCL_WRAPPER_H_
