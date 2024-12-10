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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_CONFIGS_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_CONFIGS_H_

#include <string>
#include <cstdint>

namespace mindspore {
namespace acme {
class HardwareConfig {
 public:
  HardwareConfig() = default;
  ~HardwareConfig() = default;
  HardwareConfig(uint32_t core_num, uint32_t l2_size, uint32_t l1_size, uint32_t l0a_size, uint32_t l0b_size,
                 uint32_t l0c_size, uint32_t ub_size)
      : core_num_(core_num),
        l2_size_(l2_size),
        l1_size_(l1_size),
        l0a_size_(l0a_size),
        l0b_size_(l0b_size),
        l0c_size_(l0c_size),
        ub_size_(ub_size) {}

  uint32_t core_num_{0};
  uint32_t l2_size_{0};
  uint32_t l1_size_{0};
  uint32_t l0a_size_{0};
  uint32_t l0b_size_{0};
  uint32_t l0c_size_{0};
  uint32_t hbm_bandwidth_{1};
  uint32_t l2_bandwidth_{5};
  uint32_t ub_size_{0};
};

class PlatformConfigs {
 public:
  PlatformConfigs();
  ~PlatformConfigs() = default;

  static const PlatformConfigs &GetInstance() {
    static PlatformConfigs kPlatformConfigs;
    return kPlatformConfigs;
  }

  inline uint32_t GetCoreNum() const { return hw_config_.core_num_; }

  inline uint32_t GetL2Size() const { return hw_config_.l2_size_; }

  inline uint32_t GetL1Size() const { return hw_config_.l1_size_; }

  inline uint32_t GetL0aSize() const { return hw_config_.l0a_size_; }

  inline uint32_t GetL0bSize() const { return hw_config_.l0b_size_; }

  inline uint32_t GetL0cSize() const { return hw_config_.l0c_size_; }

  inline uint32_t GetHbmBandwidth() const { return hw_config_.hbm_bandwidth_; }

  inline uint32_t GetL2BandwidthSize() const { return hw_config_.l2_bandwidth_; }

  inline uint32_t GetUbSize() const { return hw_config_.ub_size_; }

  const HardwareConfig &GetConfigByVersion(const std::string &soc_version) const;

 private:
  void Init();

  HardwareConfig hw_config_;
  std::string soc_version_;
};
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_SRC_CORE_PLATFORM_CONFIGS_H_