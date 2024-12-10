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
#ifndef LCCL_LCCL_API_H
#define LCCL_LCCL_API_H

#include <hccl.h>
#ifdef __cplusplus
extern "C" {
#endif // __cplusplus

typedef void *LcclComm;

int LcclCommInitRootInfo(uint32_t nRanks, uint32_t rank, LcclComm *comm);

int LcclCommInitAll(uint32_t ndev, int32_t* devices, LcclComm* comms);

int LcclAllReduce(int8_t *sendBuf, int8_t *recvBuf, uint64_t count, HcclDataType dataType, HcclReduceOp op,
                  LcclComm comm, aclrtStream stream);

int LcclAllGather(int8_t *sendBuf, int8_t *recvBuf, uint64_t sendCount, HcclDataType dataType, LcclComm comm,
                  aclrtStream stream);

int LcclReduceScatter(int8_t *sendBuf, int8_t *recvBuf, uint64_t recvCount, HcclDataType dataType, HcclReduceOp op,
                      LcclComm comm, aclrtStream stream);
                             
int LcclBroadcast(int8_t *buf, uint64_t count, HcclDataType dataType, uint32_t root, LcclComm comm,
                  aclrtStream stream);

int LcclCommDestroy(LcclComm comm, uint32_t ndev = 0, int32_t *devices = nullptr)

#ifdef __cplusplus
}
#endif // __cplusplus
#endif // LCCL_LCCL_API_H
