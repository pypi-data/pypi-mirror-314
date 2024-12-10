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
#ifndef MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_UTILS_H_
#include <iostream>
#include <map>
#include "include/op_param.h"
#include "utils/utils.h"
#include "acme/include/base_type.h"

namespace mindspore::internal {
static std::ostream &operator<<(std::ostream &os, const OpParam &param) {
  os << "[" << OpIdToString(param.opId) << "]";
  os << ", in dtypes: ";
  for (size_t i = 0; i < param.in_dtypes_.size(); i++) {
    os << " " << param.in_dtypes_[i];
  }
  os << "; out dtypes: ";
  for (size_t i = 0; i < param.out_dtypes_.size(); i++) {
    os << " " << param.out_dtypes_[i];
  }
  return os;
}

static std::ostream &operator<<(std::ostream &os, const DtypesParam &param) {
  os << "[" << OpIdToString(param.op_id_) << "]";
  os << ", in dtypes: ";
  for (size_t i = 0; i < param.in_dtypes_.size(); i++) {
    os << " " << param.in_dtypes_[i];
  }
  os << "; out dtypes: ";
  for (size_t i = 0; i < param.out_dtypes_.size(); i++) {
    os << " " << param.out_dtypes_[i];
  }
  return os;
}

static std::ostream &operator<<(
  std::ostream &os,
  const std::vector<std::pair<std::vector<TensorDType>, std::vector<TensorDType>>> &support_dtype_list) {
  for (auto dtyp : support_dtype_list) {
    auto ins = dtyp.first;
    auto outs = dtyp.second;
    os << "(";
    for (size_t i = 0; i < ins.size(); i++) {
      os << ins[i] << " ";
    }
    os << ",";
    for (size_t i = 0; i < outs.size(); i++) {
      os << outs[i] << " ";
    }
    os << ")";
  }
  return os;
}

static std::ostream &operator<<(std::ostream &os, const acme::DataType data_type) {
  switch (data_type) {
    case acme::DataType::kTypeUnknown:
      os << "Unknown";
      break;
    case acme::DataType::kTypeFloat16:
      os << "Float16";
      break;
    case acme::DataType::kTypeFloat32:
      os << "Float32";
      break;
    case acme::DataType::kTypeFloat64:
      os << "Float64";
      break;
    case acme::DataType::kTypeInt8:
      os << "Int8";
      break;
    case acme::DataType::kTypeInt16:
      os << "Int16";
      break;
    case acme::DataType::kTypeInt32:
      os << "Int32";
      break;
    case acme::DataType::kTypeInt64:
      os << "Int64";
      break;
    case acme::DataType::kTypeUint8:
      os << "Uint8";
      break;
    case acme::DataType::kTypeUint16:
      os << "Uint16";
      break;
    case acme::DataType::kTypeUint32:
      os << "Uint32";
      break;
    case acme::DataType::kTypeUint64:
      os << "Uint64";
      break;
    case acme::DataType::kTypeBF16:
      os << "BF16";
      break;
    case acme::DataType::kTypeBool:
      os << "Bool";
      break;
    case acme::DataType::kTypeComplex64:
      os << "Complex64";
      break;
    case acme::DataType::kTypeComplex128:
      os << "Complex128";
      break;
    case acme::DataType::kTypeString:
      os << "String";
      break;
    case acme::DataType::kTypeNone:
      os << "None";
      break;
    default:
      os << "UnknownDataType";
      break;
  }
  return os;
}

static std::ostream &operator<<(std::ostream &os, const acme::InOutDtypesList &support_dtype_list) {
  for (auto dtype_vec : support_dtype_list) {
    auto in_dtypes = dtype_vec[0];
    auto out_dtypes = dtype_vec[1];
    os << "\n[in_(";
    for (size_t i = 0; i < in_dtypes.size(); i++) {
      os << in_dtypes[i];
      if (i != in_dtypes.size() - 1) {
        os << " ";
      }
    }
    os << ")_out_(";
    for (size_t i = 0; i < out_dtypes.size(); i++) {
      os << out_dtypes[i];
      if (i != out_dtypes.size() - 1) {
        os << " ";
      }
    }
    os << ")], ";
  }
  return os;
}

static std::ostream &operator<<(std::ostream &os, const acme::ShapeInfo &shape) {
  os << "[";
  for (auto dim : shape) {
    os << dim << " ";
  }
  os << "]";
  return os;
}
}  // namespace mindspore::internal
#endif  //    MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_UTILS_H_
