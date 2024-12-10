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
#ifndef MS_KERNELS_INTERNAL_KERNEL_UTILS_KERNEL_REGISTER_H_
#define MS_KERNELS_INTERNAL_KERNEL_UTILS_KERNEL_REGISTER_H_
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <map>
#include <atomic>
#include "utils/register/kernel_creator.h"
#include "asdops/types.h"
namespace mindspore {
namespace internal {
using AsdOps::TensorDType::TENSOR_DTYPE_BF16;
using AsdOps::TensorDType::TENSOR_DTYPE_BOOL;
using AsdOps::TensorDType::TENSOR_DTYPE_DOUBLE;
using AsdOps::TensorDType::TENSOR_DTYPE_FLOAT;
using AsdOps::TensorDType::TENSOR_DTYPE_FLOAT16;
using AsdOps::TensorDType::TENSOR_DTYPE_INT16;
using AsdOps::TensorDType::TENSOR_DTYPE_INT32;
using AsdOps::TensorDType::TENSOR_DTYPE_INT64;
using AsdOps::TensorDType::TENSOR_DTYPE_INT8;
using AsdOps::TensorDType::TENSOR_DTYPE_UINT16;
using AsdOps::TensorDType::TENSOR_DTYPE_UINT32;
using AsdOps::TensorDType::TENSOR_DTYPE_UINT64;
using AsdOps::TensorDType::TENSOR_DTYPE_UINT8;
using AsdOps::TensorDType::TENSOR_DTYPE_UNDEFINED;
typedef InternalKernelImplPtr (*KernelCreator)(const OpParamPtr &param);
class InternalKernelRegistry {
 public:
  InternalKernelRegistry() = default;
  virtual ~InternalKernelRegistry() = default;

  static InternalKernelRegistry *GetInstance();
  void RegKernel(int op_id, KernelCreator creator);
  InternalKernelImplPtr GetKernel(const OpParamPtr &param);
  void SetDtypes(int op_id, std::vector<TensorDType> in_types, std::vector<TensorDType> out_types);
  void SetMutable(int op_id, bool input, bool output);
  void SetAsdDtypes(int op_id, std::vector<TensorDType> in_types, std::vector<TensorDType> out_types);
  bool IsDtypeSupported(const DtypesParamPtr &param);

 private:
  void PrintOpRegistryInfo(int op_id);
  bool IsAsdSupported(int op_id, std::vector<int64_t> &in_dtypes, std::vector<int64_t> &out_types);
  bool IsInternalSupported(int op_id, std::vector<int64_t> &in_dtypes, std::vector<int64_t> &out_types);
  std::vector<int> mutable_input_list_;
  std::vector<int> mutable_output_list_;
  std::map<int, KernelCreator> creator_list_;
  std::map<int, std::vector<std::pair<std::vector<TensorDType>, std::vector<TensorDType>>>> op_dtypes_;
  std::map<int, std::vector<std::pair<std::vector<TensorDType>, std::vector<TensorDType>>>> asd_op_dtypes_;
};

#define MUTABLE_NUM 13579
void CheckMutable(bool &input_mutable, bool &output_mutable, int remain_in, int remain_total);

class InternalKernelRegister {
 public:
  InternalKernelRegister(const int op_id, KernelCreator creator) {
    InternalKernelRegistry::GetInstance()->RegKernel(op_id, creator);
  }
  InternalKernelRegister(int op_id, int outcnt, TensorDType dt1, TensorDType dt2, TensorDType dt3);
  InternalKernelRegister(int op_id, TensorDType dt1, TensorDType dt2, TensorDType dt3, TensorDType dt4);
  InternalKernelRegister(int op_id, TensorDType main_dtype, int remain_in, int remain_total, ...);
  InternalKernelRegister(int op_id, TensorDType dtype1, TensorDType dtype2);
  InternalKernelRegister(int op_id, TensorDType dtype1, TensorDType dtype2, TensorDType dtype3);
  ~InternalKernelRegister() = default;
};
#define REG_KERNEL(op_id, creator) static InternalKernelRegister g_##op_id##kernel_reg(op_id, creator);
#define REG_KERNEL_DTYPES(op_id, incnt, outcnt, dtype, ...)                                         \
  static InternalKernelRegister g_##op_id##_##incnt##_##outcnt##_##dtype(op_id, dtype, (incnt - 1), \
                                                                         (incnt + outcnt - 1), ##__VA_ARGS__);
#define REG_KERNEL_DTYPES_WITH_NAME(name, op_id, incnt, outcnt, dtype, ...) \
  static InternalKernelRegister g_##name(op_id, dtype, (incnt - 1), (incnt + outcnt - 1), ##__VA_ARGS__);
#define REG_ROPE_DTYPES(op_id, incnt, outcnt, in_dt1, in_dt2, in_dt3, in_dt4)                                    \
  static InternalKernelRegister g_##op_id##_##incnt##_##outcnt##_##in_dt1##in_dt2(op_id, in_dt1, in_dt2, in_dt3, \
                                                                                  in_dt4);
#define REG_KERNE_BINARY_DTYPES(op_id, dt1, dt2) \
  static InternalKernelRegister g_##op_id##_##dt1##_##dt2(op_id, dt1, dt2);
#define REG_RMS_NORM_DTYPES(op_id, incnt, outcnt, in_dt1, in_dt2, out_dt1, out_dt2) \
  static InternalKernelRegister g_##op_id##_##incnt##_##outcnt##_##in_dt1##out_dt2(op_id, in_dt1, out_dt2);
#define REG_ADD_RMS_NORM_DTYPES(op_id, incnt, outcnt, in_dt1, in_dt2, in_dt3, out_dt1, out_dt2, out_dt3) \
  static InternalKernelRegister g_##op_id##_##incnt##_##outcnt##_##in_dt1##in_dt3(op_id, in_dt1, in_dt3);
#define REG_MATMUL_BIASADD_DTYPES(op_id, incnt, outcnt, in_dt1, in_dt2, in_dt3, out_dt1, ...)                     \
  static InternalKernelRegister g_##op_id##_##incnt##_##outcnt##_##in_dt1##in_dt3##out_dt1(op_id, outcnt, in_dt1, \
                                                                                           in_dt3, out_dt1);

class AsdOpInternalKernelRegister {
 public:
  AsdOpInternalKernelRegister(int op_id, TensorDType main_dtype, int remain_in, int remain_total, ...);
  AsdOpInternalKernelRegister(int op_id, TensorDType dtype1);
  AsdOpInternalKernelRegister(int op_id, TensorDType dtype1, TensorDType dtype2, TensorDType dtype3);
  AsdOpInternalKernelRegister(int op_id, TensorDType dtype1, TensorDType dtype2, TensorDType dtype3, TensorDType dtype4, TensorDType dtype5);
  AsdOpInternalKernelRegister(int op_id, TensorDType dtype1, TensorDType dtype2, TensorDType dtype3, TensorDType dtype4,
                              TensorDType dtype5, TensorDType dtype6, TensorDType dtype7, TensorDType dtype8);
  ~AsdOpInternalKernelRegister() = default;
};
#define REG_ASD_KERNEL_DTYPES(op_id, incnt, outcnt, dtype, ...)                    \
  static AsdOpInternalKernelRegister g_asd_##op_id##_##incnt##_##outcnt##_##dtype( \
    op_id, dtype, (incnt - 1), (incnt + outcnt - 1), ##__VA_ARGS__);
#define REG_ASD_NORM_KERNEL_DTYPES(op_id, incnt, outcnt, dt1) \
  static AsdOpInternalKernelRegister g_asd_##op_id##_##dt1(op_id, dt1);
#define REG_ASD_GATHER_KERNEL_DTYPES(op_id, incnt, outcnt, dt1, dt2, dt3) \
  static AsdOpInternalKernelRegister g_asd_##op_id##incnt##outcnt##dt1##dt2##dt3(op_id, dt1, dt2, dt3);

bool InternalKernelEnableByEnv(const int op_id);
}  // namespace internal
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_UTILS_KERNEL_REGISTER_H_
