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
#ifndef COMMON_RT_BASE_TYPES_H
#define COMMON_RT_BASE_TYPES_H
#include <cstdint>
#include <string>

#ifdef __cplusplus
extern "C" {
#endif

typedef void *AsdDevice;
typedef void *AsdRtStream;

typedef enum {
    ASDRT_SUCCESS = 0,
    ASDRT_ERROR_NOT_INITIALIZED = -1,
    ASDRT_ERROR_NOT_IMPLMENT = -2,
    ASDRT_ERROR_ASCEND_ENV_NOT_EXIST = -3,
    ASDRT_ERROR_LOAD_RUNTIME_FAIL = -4,
    ASDRT_ERROR_FUNC_NOT_EXIST = -5,
    ASDRT_ERROR_OPEN_BIN_FILE_FAIL = -6,
    ASDRT_ERROR_PARA_CHECK_FAIL = -7,
} AsdRtError;

typedef enum {
    ASDRT_MEMCOPY_HOST_TO_HOST = 0,
    ASDRT_MEMCOPY_HOST_TO_DEVICE,
    ASDRT_MEMCOPY_DEVICE_TO_HOST,
    ASDRT_MEMCOPY_DEVICE_TO_DEVICE, // device to device, 1P &P2P
    ASDRT_MEMCOPY_MANAGED,
    ASDRT_MEMCOPY_ADDR_DEVICE_TO_DEVICE,
    ASDRT_MEMCOPY_HOST_TO_DEVICE_EX, // host to device ex(only used for 8 bytes)
    ASDRT_MEMCOPY_DEVICE_TO_HOST_EX, // device to host ex
} AsdRtMemCopyType;

typedef enum {
    ASDRT_MEM_DEFAULT = 0,    // default memeory on device
    ASDRT_MEM_HBM = 0x2,      // HBM memory on device
    ASDRT_MEM_RDMA_HBM = 0x3, // RDMA-HBM memory on device
    ASDRT_MEM_DDR = 0x4,      // DDR memory on device
    ASDRT_MEM_SPM = 0x8,      // shaed physical memory on device
    ASDRT_MEM_P2P_HBM = 0x10, // HBM memory on other 4p device
    ASDRT_MEM_P2P_DDR = 0x11, // DDR memory on other device
    ASDRT_MEM_DDR_NC = 0x20,  // DDR memory of non-cache
    ASDRT_MEM_TS_4G = 0x40,
    ASDRT_MEM_TS = 0x80,
    ASDRT_MEM_HOST = 0x81, // memory on host
    ASDRT_MEM_RESERVED = 0x100,
    ASDRT_MEM_L1 = (0x1 << 16),
    ASDRT_MEM_L2 = (0x1 << 17),
} AsdRtMemType;

typedef void *AsdRtModule;

typedef enum {
    ASDRT_MODULE_OBJECT = 0, // 原始object文件
    ASDRT_MODULE_BIN = 1,    // bin头 + 连续原始object
    ASDRT_MODULE_FUSEIO_BIN  // fusionbin头 + 连续的bin
} AsdRtModuleType;

typedef struct {
    AsdRtModuleType type = ASDRT_MODULE_OBJECT;
    uint32_t version = 0;
    const void *data = nullptr;
    uint64_t dataLen = 0;
    uint32_t magic = 0x41494343U;
} AsdRtModuleInfo;

typedef struct {
    uint32_t addrOffset{0};
    uint32_t dataOffset{0};
} RtHostInputInfoT;

typedef struct {
    void *args{nullptr};
    RtHostInputInfoT *hostInputInfoPtr{nullptr};
    uint32_t argsSize{0};
    uint32_t tilingAddrOffset{0};
    uint32_t tilingDataOffset{0};
    uint16_t hostInputInfoNum{0};
    uint8_t hasTiling{0};
    uint8_t isNoNeedH2DCopy{0};
    uint8_t reserved[4] = {0};
} RtArgsExT;

typedef struct {
    uint8_t qos{0};
    uint8_t partId{0};
    uint8_t schemMode{0};
    uint8_t res[1] = {0};
} RtTaskCfgInfoT;

typedef struct {
    uint64_t tilingId = 0;
    uint32_t blockDim = 0;
    void *args = nullptr;
    uint32_t argSize = 0;
    RtArgsExT *argsEx = nullptr;
} AsdRtKernelParam;

#ifdef __cplusplus
}
#endif
#endif
