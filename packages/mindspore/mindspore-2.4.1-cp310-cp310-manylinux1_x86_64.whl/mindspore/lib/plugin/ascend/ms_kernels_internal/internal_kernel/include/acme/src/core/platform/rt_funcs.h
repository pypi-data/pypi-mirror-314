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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_RT_FUNCS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_RT_FUNCS_H_

#include "acme/include/base_type.h"

#ifdef __cplusplus
extern "C" {
#endif

#define RT_DEV_BINARY_MAGIC_ELF 0x43554245U
#define RT_DEV_BINARY_MAGIC_ELF_AIVEC 0x41415246U
#define RT_DEV_BINARY_MAGIC_ELF_AICUBE 0x41494343U

typedef void *rtStream_t;

typedef enum {
  INTERNAL_RTSUCCESS = 0,
  INTERNAL_RTERROR_NOT_INITIALIZED = -1,
  INTERNAL_RTERROR_NOT_IMPLMENT = -2,
  INTERNAL_RTERROR_ASCEND_ENV_NOT_EXIST = -3,
  INTERNAL_RTERROR_LOAD_RUNTIME_FAIL = -4,
  INTERNAL_RTERROR_FUNC_NOT_EXIST = -5,
  INTERNAL_RTERROR_OPEN_BIN_FILE_FAIL = -6,
  INTERNAL_RTERROR_PARA_CHECK_FAIL = -7,
} RtError;

typedef enum tagRtError {
  RT_ERROR_NONE = 0x0,                      // success
  RT_ERROR_INVALID_VALUE = 0x1,             // invalid value
  RT_ERROR_MEMORY_ALLOCATION = 0x2,         // memory allocation fail
  RT_ERROR_INVALID_RESOURCE_HANDLE = 0x3,   // invalid handle
  RT_ERROR_INVALID_DEVICE_POINTER = 0x4,    // invalid device point
  RT_ERROR_INVALID_MEMCPY_DIRECTION = 0x5,  // invalid memory copy dirction
  RT_ERROR_INVALID_DEVICE = 0x6,            // invalid device
  RT_ERROR_NO_DEVICE = 0x7,                 // no valid device
  RT_ERROR_CMD_OCCUPY_FAILURE = 0x8,        // command occpuy failure
  RT_ERROR_SET_SIGNAL_FAILURE = 0x9,        // set signal failure
  RT_ERROR_UNSET_SIGNAL_FAILURE = 0xA,      // unset signal failure
  RT_ERROR_OPEN_FILE_FAILURE = 0xB,         // unset signal failure
  RT_ERROR_WRITE_FILE_FAILURE = 0xC,
  RT_ERROR_MEMORY_ADDRESS_UNALIGNED = 0xD,
  RT_ERROR_DRV_ERR = 0xE,
  RT_ERROR_LOST_HEARTBEAT = 0xF,
  RT_ERROR_REPORT_TIMEOUT = 0x10,
  RT_ERROR_NOT_READY = 0x11,
  RT_ERROR_DATA_OPERATION_FAIL = 0x12,
  RT_ERROR_INVALID_L2_INSTR_SIZE = 0x13,
  RT_ERROR_DEVICE_PROC_HANG_OUT = 0x14,
  RT_ERROR_DEVICE_POWER_UP_FAIL = 0x15,
  RT_ERROR_DEVICE_POWER_DOWN_FAIL = 0x16,
  RT_ERROR_FEATURE_NOT_SUPPROT = 0x17,
  RT_ERROR_KERNEL_DUPLICATE = 0x18,             // register same kernel repeatly
  RT_ERROR_MODEL_STREAM_EXE_FAILED = 0x91,      // the model stream failed
  RT_ERROR_MODEL_LOAD_FAILED = 0x94,            // the model stream failed
  RT_ERROR_END_OF_SEQUENCE = 0x95,              // end of sequence
  RT_ERROR_NO_STREAM_CB_REG = 0x96,             // no callback register info for stream
  RT_ERROR_DATA_DUMP_LOAD_FAILED = 0x97,        // data dump load info fail
  RT_ERROR_CALLBACK_THREAD_UNSUBSTRIBE = 0x98,  // callback thread unsubstribe
  RT_ERROR_RESERVED
} rtError_t;

// rt kernel
typedef struct {
  uint32_t magic{0};
  uint32_t version{0};
  const void *data{nullptr};
  uint64_t length{0};
} RtDevBinary_T;

typedef void *rtStream_t;

using RtDevBinaryRegisterFunc = rtError_t (*)(const RtDevBinary_T *bin, void **hdl);
using RtFunctionRegisterFunc = rtError_t (*)(void *binHandle, const void *subFunc, const char *stubName,
                                             const void *kernelInfoExt, uint32_t funcMode);
using RtKernelLaunchFunc = rtError_t (*)(const void *stubFunc, uint32_t blockDim, void *args, uint32_t argsSize,
                                         void *smDesc, rtStream_t sm);
using RtGetC2cCtrlAddrFunc = rtError_t (*)(uint64_t *addr, uint32_t *len);

using RtGetSocVersionFunc = int (*)(char *version, uint32_t maxLen);

#ifdef __cplusplus
}
#endif

namespace mindspore {
namespace acme {
class RtFuncs {
 public:
  RtFuncs();
  ~RtFuncs() = default;

  static const RtFuncs &GetInstance() {
    static RtFuncs kRtFuncs;
    return kRtFuncs;
  }

  inline RtDevBinaryRegisterFunc GetRtDevBinaryRegisterFunc() const { return rt_dev_bin_reg_func_; }

  inline RtFunctionRegisterFunc GetRtFunctionRegisterFunc() const { return rt_func_reg_func_; }

  inline RtKernelLaunchFunc GetRtKernelLaunchFunc() const { return rt_kernel_launch_func_; }

  inline RtGetC2cCtrlAddrFunc GetRtGetC2cCtrlAddrFunc() const { return rt_get_c2c_ctrl_addr_func_; }

  std::string GetSocVersion() const;

 private:
  void Init();

  RtDevBinaryRegisterFunc rt_dev_bin_reg_func_{nullptr};
  RtFunctionRegisterFunc rt_func_reg_func_{nullptr};
  RtKernelLaunchFunc rt_kernel_launch_func_{nullptr};
  RtGetC2cCtrlAddrFunc rt_get_c2c_ctrl_addr_func_{nullptr};
  RtGetSocVersionFunc rt_get_soc_version_func_{nullptr};
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_RT_FUNCS_H_