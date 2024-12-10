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
#ifndef ASDRT_BACKEND_BACKEND_H
#define ASDRT_BACKEND_BACKEND_H
#include "asdops/utils/rt/base/types.h"

namespace AsdOps {
class Backend {
public:
    Backend();
    virtual ~Backend();

public:
    virtual int DeviceGetCount(int32_t *devCount) = 0;
    virtual int DeviceGetIds(int32_t *devIds, int32_t devIdNum) = 0;
    virtual int DeviceGetCurrent(int32_t *devId) = 0;
    virtual int DeviceSetCurrent(int32_t devId) = 0;
    virtual int DeviceResetCurrent(int32_t devId) = 0;
    virtual int DeviceSetSocVersion(const char *version) = 0;
    virtual int DeviceGetSocVersion(char *version, uint32_t maxLen) = 0;
    virtual int DeviceGetBareTgid(uint32_t *pid) = 0;
    virtual int DeviceGetPairDevicesInfo(uint32_t devId, uint32_t otherDevId, int32_t infoType, int64_t *val) = 0;

public:
    virtual int StreamCreate(AsdRtStream *stream, int32_t priority) = 0;
    virtual int StreamDestroy(AsdRtStream stream) = 0;
    virtual int StreamSynchronize(AsdRtStream stream) = 0;
    virtual int StreamGetId(AsdRtStream stream, int32_t *streamId) = 0;

public:
    virtual int MemMallocDevice(void **devPtr, uint64_t size, AsdRtMemType memType = ASDRT_MEM_DEFAULT) = 0;
    virtual int MemFreeDevice(void *devPtr) = 0;
    virtual int MemMallocHost(void **hostPtr, uint64_t size) = 0;
    virtual int MemFreeHost(void *hostPtr) = 0;
    virtual int MemCopy(void *dst, uint64_t dstLen, const void *srcPtr, uint64_t srcLen,
                        AsdRtMemCopyType copyType) = 0;
    virtual int MemCopyAsync(void *dst, uint64_t dstLen, const void *srcPtr, uint64_t srcLen,
                             AsdRtMemCopyType copyType, void *stream) = 0;
    virtual int MemSetAsync(void *dst, uint64_t destMax, uint32_t value, uint64_t count, void *stream) = 0;
    virtual int IpcSetMemoryName(const void *ptr, uint64_t byteCount, const char *name, uint32_t len) = 0;
    virtual int IpcOpenMemory(void **ptr, const char *name) = 0;
    virtual int SetIpcMemPid(const char *name, int32_t pid[], int num) = 0;

public:
    virtual int ModuleCreate(AsdRtModuleInfo *moduleInfo, AsdRtModule *module) = 0;
    virtual int ModuleCreateFromFile(const char *moduleFilePath, AsdRtModuleType type, int version,
                                     AsdRtModule *module) = 0;
    virtual int ModuleDestory(AsdRtModule *module) = 0;
    virtual int ModuleBindFunction(AsdRtModule module, const char *funcName, void *func) = 0;
    virtual int RegisterAllFunction(AsdRtModuleInfo *moduleInfo, void **handle) = 0;
    virtual int FunctionLaunch(const void *func, const AsdRtKernelParam *param, AsdRtStream stream) = 0;
    virtual int FunctionLaunchWithHandle(void *handle, const AsdRtKernelParam *param, AsdRtStream stream,
                                         const RtTaskCfgInfoT *cfgInfo) = 0;
    virtual int FunctionLaunchWithFlag(const void *func, const AsdRtKernelParam *param, AsdRtStream stream,
                                       const RtTaskCfgInfoT *cfgInfo) = 0;

public:
    virtual int GetC2cCtrlAddr(uint64_t *addr, uint32_t *len) = 0;
};
}

#endif