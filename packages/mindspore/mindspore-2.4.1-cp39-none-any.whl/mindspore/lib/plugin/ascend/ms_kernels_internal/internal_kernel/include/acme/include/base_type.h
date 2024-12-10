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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ACME_BASE_TYPE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ACME_BASE_TYPE_H_

#include <vector>
#include <map>
#include <cstdint>
#include <memory>

namespace mindspore {
namespace acme {
using ShapeInfo = std::vector<int64_t>;

enum DataType : int {
  kTypeUnknown = 0,
  kTypeFloat16,
  kTypeFloat32,
  kTypeFloat64,
  kTypeInt8,
  kTypeInt16,
  kTypeInt32,
  kTypeInt64,
  kTypeUint8,
  kTypeUint16,
  kTypeUint32,
  kTypeUint64,
  kTypeBF16,
  kTypeBool,
  kTypeComplex64,
  kTypeComplex128,
  kTypeString,
  kTypeNone,
};

enum TensorFormat : int {
  kFormatUnknown,
  kFormatND,
  kFormatNCHW,
  kFormatNHWC,
  kFormatNC1HWC0,
  kFormatFRACTAL_Z,
  kFormatNC1HWC0_C04,
  kFormatHWCN,
  kFormatNDHWC,
  kFormatFRACTAL_NZ,
  kFormatNCDHW,
  kFormatNDC1HWC0,
  kFormatFRACTAL_Z_3D
};

enum AcmeStatus {
  kAcmeOk = 0,
  kAcmeError,
};

class ArgImmutableInfo {
 public:
  ArgImmutableInfo(DataType type, TensorFormat format) : d_type_(type), format_(format) {}
  ArgImmutableInfo() {}
  ~ArgImmutableInfo() = default;

  void SetDtype(DataType type) { d_type_ = type; }

  DataType GetDtype() const { return d_type_; }

  void SetFormat(TensorFormat format) { format_ = format; }

  TensorFormat GetFormat() const { return format_; }

 private:
  DataType d_type_{DataType::kTypeUnknown};
  TensorFormat format_{TensorFormat::kFormatUnknown};
};

class ArgDesc {
 public:
  ArgDesc(const ArgImmutableInfo &arg_ii) : immutable_info_(arg_ii) {}
  ArgDesc(DataType type, TensorFormat format) : immutable_info_(type, format) {}
  ArgDesc(const ShapeInfo &shape, DataType type, TensorFormat format) : shape_(shape), immutable_info_(type, format) {}

  ~ArgDesc() = default;
  const ShapeInfo &GetShape() const { return shape_; }

  void SetShape(const ShapeInfo &shape) { shape_ = shape; }

  void SetDtype(DataType type) { immutable_info_.SetDtype(type); }

  DataType GetDtype() const {
    return immutable_info_.GetDtype();
    ;
  }

  void SetFormat(TensorFormat format) { immutable_info_.SetFormat(format); }

  TensorFormat GetFormat() const {
    return immutable_info_.GetFormat();
    ;
  }

  const ArgImmutableInfo &GetImmutableInfo() const { return immutable_info_; }

  inline size_t ElementNum() const {
    if (shape_.empty()) {
      return 0;
    }

    size_t num = 1;
    for (auto s : shape_) {
      num *= static_cast<size_t>(s);
    }

    return num;
  }

 private:
  ShapeInfo shape_{0};
  ArgImmutableInfo immutable_info_;
};
using ArgDescPtr = std::shared_ptr<ArgDesc>;

using InputsDescList = std::vector<ArgDesc>;
using OutputsDescList = std::vector<ArgDesc>;
using InputsImmutableInfoList = std::vector<ArgImmutableInfo>;
using OutputsImmutableInfoList = std::vector<ArgImmutableInfo>;
using InputDataTypes = std::vector<DataType>;
using DtypeInfoList = std::vector<DataType>;
using RawDeviceAddr = void *;
using RawHostAddr = void *;
using InputsAddrList = std::vector<RawDeviceAddr>;
using OutputsAddrList = std::vector<RawDeviceAddr>;
using WsAddrList = std::vector<RawDeviceAddr>;
using ShapeInfoList = std::vector<ShapeInfo>;

using InOutDtypesList = std::vector<std::vector<InputDataTypes>>;
using InOutDtypesTargetMap = std::map<std::string, InOutDtypesList>;
}  // namespace acme
}  // namespace mindspore

#endif  // MS_KERNELS_INTERNAL_KERNEL_ACME_BASE_TYPE_H_