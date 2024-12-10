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
#ifndef ASDOPS_RUNINFO_H
#define ASDOPS_RUNINFO_H

#include <cstdint>

#include "asdops/kernel_info.h"
#include "asdops/utils/noncopyable/noncopyable.h"

namespace AsdOps {
class RunInfo : public NonCopyable {
public:
    RunInfo() = default;
    ~RunInfo();

public:
    void Reset();

    void SetStream(void *stream);
    void *GetStream() const;

    void SetLaunchWithTiling(bool flag);
    bool GetLaunchWithTiling() const;

    size_t GetWorkspaceSize() const;
    void SetWorkspaceDeviceAddr(uint8_t *addr);
    uint8_t *GetWorkspaceDeviceAddr() const;

    void SetTilingHostAddr(uint8_t *addr, uint64_t len);
    void SetTilingDeviceAddr(uint8_t *addr);
    uint8_t *GetTilingDeviceAddr() const;

    KernelInfo &GetKernelInfo();

    std::string ToString() const;

    void CopyTo(RunInfo &runInfo) const;

private:
    // used by User
    bool launchWithTiling_ = true;
    void *stream_ = nullptr;
    uint8_t *workspaceAddr_ = nullptr;
    uint8_t *tilingDeviceAddr_ = nullptr;

    // used by Tactic
    KernelInfo kernelInfo_;
};
} // namespace AsdOps

#endif
