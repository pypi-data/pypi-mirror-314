/*
 * Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.
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
#ifndef LACL_LCCL_H
#define LACL_LCCL_H

#include <lcal_comm.h>


namespace Lcal {
class Lccl {
public:
    Lccl(LcalComm &comm);
    ~Lccl();
    int Init(const std::string &uid = "", int maxBuffSize = LCAL_BUFF_BYTES);
    int InitThread();
    int AllReduce(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType,
        HcclReduceOp op = HCCL_REDUCE_SUM, aclrtStream stream = nullptr);
    int ReduceScatter(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType,
        HcclReduceOp op = HCCL_REDUCE_SUM, aclrtStream stream = nullptr);
    int AllGather(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType, aclrtStream stream = nullptr);
    int All2All(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType, aclrtStream stream = nullptr);
    int Broadcast(void *buff, int64_t count, HcclDataType dataType, int32_t root, aclrtStream stream = nullptr);

private:
    bool CheckDataType(const HcclDataType &dataType) const;
    int LoopBack(void *sendBuff, void *recvBuff, int64_t count, HcclDataType dataType);

private:
    LcalComm &comm_;
    int rank_ = 0;
    int rankSize_ = 0;
};
}
#endif // LACL_LCCL_H
