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
#ifndef COMMON_RT_MODULE_MODULE_H
#define COMMON_RT_MODULE_MODULE_H

#include "asdops/utils/rt/base/types.h"

#ifdef __cplusplus
extern "C" {
#endif
namespace AsdOps {
int AsdRtModuleCreate(AsdRtModuleInfo *moduleInfo, AsdRtModule *module);
int AsdRtModuleCreateFromFile(const char *moduleFilePath, AsdRtModuleType type, int version, AsdRtModule *module);
int AsdRtModuleDestory(AsdRtModule *module);
int AsdRtModuleBindFunction(AsdRtModule module, const char *funcName, void *func);
int AstRtRegisterAllFunction(AsdRtModuleInfo *moduleInfo, void **handle);
int AsdRtFunctionLaunch(const void *func, const AsdRtKernelParam *launchParam, AsdRtStream stream);
int AsdRtFunctionLaunchWithHandle(void *handle, const AsdRtKernelParam *launchParam, AsdRtStream stream,
    const RtTaskCfgInfoT *cfgInfo);
int AsdRtFunctionLaunchWithFlag(const void *func, const AsdRtKernelParam *launchParam, AsdRtStream stream,
    const RtTaskCfgInfoT *cfgInfo);
}
#ifdef __cplusplus
}
#endif
#endif