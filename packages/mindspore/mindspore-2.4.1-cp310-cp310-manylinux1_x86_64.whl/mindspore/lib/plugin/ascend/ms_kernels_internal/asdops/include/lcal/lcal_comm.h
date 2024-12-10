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
#ifndef LCAL_COMM_H
#define LCAL_COMM_H

#include <vector>
#include <string>
#include <unordered_map>

#include <lcal_types.h>
#include <hccl.h>
class ShareMemory;

namespace Lcal {
constexpr int IPC_NAME_SIZE = 65;
constexpr int SINGLE_MACHINE_910B2C_RANK_SIZE = 16;


struct ExtraFlag {
    static constexpr uint32_t RDMA = 1;
    static constexpr uint32_t TOPO_910B2C = 1 << 1;
    static constexpr uint32_t TOPO_910C = 1 << 2;
    static constexpr uint32_t DETERMINISTIC = 1 << 3;
    static constexpr uint32_t QUANT_FP16 = 1 << 4;
    static constexpr uint32_t QUANT_FP32 = 1 << 5;
};

struct CommArgs {
    void SetBuff(int8_t *b[LCAL_MAX_RANK_SIZE])
    {
        for (int i = 0; i < rankSize; ++i) {
            peerMems[i] = b[i];
        }
    }
    int rank = 0;           // attr rank_id
    int rankSize = 0;
    uint32_t extraFlag = 0; // 32 bit map，具体每一位的含义就在此文件正上方
    int8_t *peerMems[LCAL_MAX_RANK_SIZE] = {}; // 传入初始化获得的buff，所有allreduce都是同一个参数
    int64_t sendCountMatrix[LCAL_MAX_RANK_SIZE * LCAL_MAX_RANK_SIZE] = {}; // for all2all
};

class LcalComm {
public:
    LcalComm(int rank, int rankSize, int devId = -1, const std::vector<int> &devList = {});
    ~LcalComm();
    LcalComm(const LcalComm &) = delete;
    LcalComm &operator=(const LcalComm &) = delete;
    int Init(const std::string &uid = "", int maxBuffSize = LCAL_BUFF_BYTES);
    int InitThread();
    int GetRank() const;
    int GetRankSize() const;
    const PhysicalInfo &GetPhysicalInfo() const;
    friend class Lccl;
    friend class Lcoc;
    friend class LcclTest;

private:
    int SetIpcPid(const char *name, const uint32_t *pids) const;
    int OpenIpcMem(const char names[LCAL_MAX_RANK_SIZE][IPC_NAME_SIZE]);
    int GetDev(ShareMemory *shm);
    int GetDevThread();
    int EnablePeerAccess();
    int InitCommMem(int maxBuffSize, ShareMemory *shm);
    int InitCommon();
    void FreePeerMem(int8_t *&mem) const;
    ChipName GetChipName() const;

private:
    std::string shmName_ = "lccl";
    int rank_ = 0;
    int rankSize_ = 0;
    int localHostNpuNum_ = 0;
    int devId_ = 0;
    bool inited_ = false;
    std::vector<int> devList_;
    int8_t *peerMem_[LCAL_MAX_RANK_SIZE] = {}; // shared ping pong buff
    std::unordered_map<std::string, const char *> kernelNameMap_;
    PhysicalInfo physicalInfo_ = {};
    CommArgs commArgs_ = {};
    int8_t *commArgsPtr_ = nullptr;
    bool deterministic_ = false;
};
} // Lcal

#endif // LCAL_COMM_H
