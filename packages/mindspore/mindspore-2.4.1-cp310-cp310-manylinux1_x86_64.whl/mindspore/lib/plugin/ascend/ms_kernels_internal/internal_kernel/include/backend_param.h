/**
 * Copyright 2023-2024 Huawei Technologies Co., Ltd
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
#ifndef BACKEND_PARAM_H_
#define BACKEND_PARAM_H_
namespace mindspore {
namespace internal {

struct HardwareInfo {
  uint32_t coreNum{0};
  uint32_t l2Size{0};
  uint32_t l1Size{0};
  uint32_t l0aSize{0};
  uint32_t l0bSize{0};
  uint32_t l0cSize{0};
  uint32_t hbmBandWidth{1};
  uint32_t l2BandWidth{5};
  uint32_t ubSize{0};
};

static void GetHardwareInfoPPMatmul910B1(HardwareInfo &hwInfo) {
  hwInfo.coreNum = 24;
  hwInfo.l2Size = 201326592;
  hwInfo.l1Size = 524288;
  hwInfo.l0aSize = 65536;
  hwInfo.l0bSize = 65536;
  hwInfo.l0cSize = 131072;
  hwInfo.ubSize = 196608;
}

static void GetHardwareInfoPPMatmul910B2(HardwareInfo &hwInfo) {
  hwInfo.coreNum = 24;
  hwInfo.l2Size = 201326592;
  hwInfo.l1Size = 524288;
  hwInfo.l0aSize = 65536;
  hwInfo.l0bSize = 65536;
  hwInfo.l0cSize = 131072;
  hwInfo.ubSize = 196608;
}

static void GetHardwareInfoPPMatmul910B3(HardwareInfo &hwInfo) {
  hwInfo.coreNum = 20;
  hwInfo.l2Size = 201326592;
  hwInfo.l1Size = 524288;
  hwInfo.l0aSize = 65536;
  hwInfo.l0bSize = 65536;
  hwInfo.l0cSize = 131072;
  hwInfo.ubSize = 196608;
}

static void GetHardwareInfoPPMatmul910B4(HardwareInfo &hwInfo) {
  hwInfo.coreNum = 20;
  hwInfo.l2Size = 100663296;
  hwInfo.l1Size = 524288;
  hwInfo.l0aSize = 65536;
  hwInfo.l0bSize = 65536;
  hwInfo.l0cSize = 131072;
  hwInfo.ubSize = 196608;
}
}  // namespace internal
}  // namespace mindspore
#endif
