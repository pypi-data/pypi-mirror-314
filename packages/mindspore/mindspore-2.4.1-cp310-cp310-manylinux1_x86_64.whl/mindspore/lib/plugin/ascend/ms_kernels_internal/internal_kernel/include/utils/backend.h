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
#ifndef MS_KERNELS_INTERNAL_SRC_UTILS_BACKEND_H_
#define MS_KERNELS_INTERNAL_SRC_UTILS_BACKEND_H_

#include "include/backend_param.h"
#include "acme/src/core/platform/platform_configs.h"

namespace mindspore {
namespace internal {
inline void GetHardwareInfo(HardwareInfo &hwInfo, std::string soc) {
  if (soc == "Ascend910B2" || soc == "Ascend910B2C") {
    GetHardwareInfoPPMatmul910B2(hwInfo);
  } else if (soc == "Ascend910B1") {
    GetHardwareInfoPPMatmul910B1(hwInfo);
  } else if (soc == "Ascend910B3") {
    GetHardwareInfoPPMatmul910B3(hwInfo);
  } else if (soc == "Ascend910B4") {
    GetHardwareInfoPPMatmul910B4(hwInfo);
  }
}
inline int GetCoreNum(std::string soc) {
  return acme::PlatformConfigs::GetInstance().GetCoreNum();
}
inline uint32_t GetMaxUbSize(std::string soc) {
  HardwareInfo hwInfo;
  GetHardwareInfo(hwInfo, soc);
  return hwInfo.ubSize;
}
}  // namespace internal
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_SRC_UTILS_BACKEND_H_
