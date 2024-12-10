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

#ifndef MS_KERNELS_INTERNAL_KERNEL_SRC_ACME_UTILS_PROFILING_UTIL_H_
#define MS_KERNELS_INTERNAL_KERNEL_SRC_ACME_UTILS_PROFILING_UTIL_H_

#include <string>
#include <vector>
#include <map>
#include "include/ms_int_types.h"
#include "acme/include/base_type.h"
#include "msprof/toolchain/prof_api.h"
#include "msprof/toolchain/prof_data_config.h"
#include "msprof/toolchain/prof_common.h"
#include "utils/log/log.h"

namespace mindspore {
namespace acme {
struct TensorInfoWrapper {
  MsprofAdditionalInfo tensor_info;
  uint64_t tensor_num;
};

struct ProfNodeAdditionInfo {
  MsprofCompactInfo node_basic_info;
  std::vector<TensorInfoWrapper> tensor_info_wrappers;
  MsprofApi api;
};

// format
constexpr auto kOpFormat_DEFAULT = "DefaultFormat";
constexpr auto kOpFormat_ChannelFirst = "ChannelFirst";
constexpr auto kOpFormat_ChannelLast = "ChannelLast";
constexpr auto kOpFormat_NC1KHKWHWC0 = "NC1KHKWHWC0";
constexpr auto kOpFormat_ND = "ND";
constexpr auto kOpFormat_NCHW = "NCHW";
constexpr auto kOpFormat_NHWC = "NHWC";
constexpr auto kOpFormat_HWCN = "HWCN";
constexpr auto kOpFormat_CHWN = "CHWN";
constexpr auto kOpFormat_NC1HWC0 = "NC1HWC0";
constexpr auto kOpFormat_FRAC_Z = "FRACTAL_Z";
constexpr auto kOpFormat_FRACTAL_Z = "FRACTAL_Z";
constexpr auto kOpFormat_FRAC_NZ = "FRACTAL_NZ";
constexpr auto kOpFormat_C1HWNCoC0 = "C1HWNCoC0";
constexpr auto kOpFormat_NC1HWC0_C04 = "NC1HWC0_C04";
constexpr auto kOpFormat_FRACTAL_Z_C04 = "FRACTAL_Z_C04";
constexpr auto kOpFormat_NDHWC = "NDHWC";
constexpr auto kOpFormat_NCDHW = "NCDHW";
constexpr auto kOpFormat_DHWNC = "DHWNC";
constexpr auto kOpFormat_DHWCN = "DHWCN";
constexpr auto kOpFormat_NDC1HWC0 = "NDC1HWC0";
constexpr auto kOpFormat_FRACTAL_Z_3D = "FRACTAL_Z_3D";
constexpr auto kOpFormat_FRACTAL_ZN_LSTM = "FRACTAL_ZN_LSTM";
constexpr auto kOpFormat_FRACTAL_ZN_RNN = "FRACTAL_ZN_RNN";
constexpr auto kOpFormat_ND_RNN_BIAS = "ND_RNN_BIAS";

// reference: msprof/analysis/csrc/viewer/database/drafts/number_mapping.cpp
enum FormatMs : int {
  NCHW = 0,
  NHWC = 1,
  FORMAT_ND = 2,
  NC1HWC0 = 3,
  FRACTAL_Z = 4,
  NC1C0HWPAD = 5,
  NHWC1C0 = 6,
  FSR_NCHW = 7,
  FRACTAL_DECONV = 8,
  C1HWNC0 = 9,
  FRACTAL_DECONV_TRANSPOSE = 10,
  FRACTAL_DECONV_SP_STRIDE_TRANS = 11,
  NC1HWC0_C04 = 12,
  FRACTAL_Z_C04 = 13,
  CHWN = 14,
  FRACTAL_DECONV_SP_STRIDE8_TRANS = 15,
  HWCN = 16,
  NC1KHKWHWC0 = 17,
  BN_WEIGHT = 18,
  FILTER_HWCK = 19,
  HASHTABLE_LOOKUP_LOOKUPS = 20,
  HASHTABLE_LOOKUP_KEYS = 21,
  HASHTABLE_LOOKUP_VALUE = 22,
  HASHTABLE_LOOKUP_OUTPUT = 23,
  HASHTABLE_LOOKUP_HITS = 24,
  C1HWNCoC0 = 25,
  FORMAT_MD = 26,
  NDHWC = 27,
  FRACTAL_ZZ = 28,
  FRACTAL_NZ = 29,
  NCDHW = 30,
  DHWCN = 31,
  NDC1HWC0 = 32,
  FRACTAL_Z_3D = 33,
  FORMAT_CN = 34,
  FORMAT_NC = 35,
  DHWNC = 36,
  FRACTAL_Z_3D_TRANSPOSE = 37,
  FRACTAL_ZN_LSTM = 38,
  FRACTAL_Z_G = 39,
  RESERVED = 40,
  ALL = 41,
  // NULL = 42,
  ND_RNN_BIAS = 43,
  FRACTAL_ZN_RNN = 44,
  END = 45,
  FORMAT_NCL = 47,
  MAX = 0xff,
  UNKNOWN_ = 200,
  DEFAULT_ = 201,
  NC1KHKWHWC0_ = 202,
  ND_ = 203,
  NCHW_ = 204,
  NHWC_ = 205,
  HWCN_ = 206,
  NC1HWC0_ = 207,
  FRAC_Z_ = 208,
  C1HWNCOC0_ = 209,
  FRAC_NZ_ = 210,
  NC1HWC0_C04_ = 211,
  FRACTAL_Z_C04_ = 212,
  NDHWC_ = 213,
  FRACTAL_ZN_LSTM_ = 214,
  FRACTAL_ZN_RNN_ = 215,
  ND_RNN_BIAS_ = 216,
  NDC1HWC0_ = 217,
  NCDHW_ = 218,
  FRACTAL_Z_3D_ = 219,
  DHWNC_ = 220,
  DHWCN_ = 221,
};
// 0 means unknown format
static std::map<std::string, uint32_t> OpFormat2Index{{kOpFormat_DEFAULT, FormatMs::DEFAULT_},
                                                      {kOpFormat_NC1KHKWHWC0, FormatMs::NC1KHKWHWC0_},
                                                      {kOpFormat_ND, FormatMs::ND_},
                                                      {kOpFormat_NCHW, FormatMs::NCHW_},
                                                      {kOpFormat_NHWC, FormatMs::NHWC_},
                                                      {kOpFormat_HWCN, FormatMs::HWCN_},
                                                      {kOpFormat_NC1HWC0, FormatMs::NC1HWC0_},
                                                      {kOpFormat_FRAC_Z, FormatMs::FRAC_Z_},
                                                      {kOpFormat_C1HWNCoC0, FormatMs::C1HWNCOC0_},
                                                      {kOpFormat_FRAC_NZ, FormatMs::FRAC_NZ_},
                                                      {kOpFormat_NC1HWC0_C04, FormatMs::NC1HWC0_C04_},
                                                      {kOpFormat_FRACTAL_Z_C04, FormatMs::FRACTAL_Z_C04_},
                                                      {kOpFormat_NDHWC, FormatMs::NDHWC_},
                                                      {kOpFormat_FRACTAL_ZN_LSTM, FormatMs::FRACTAL_ZN_LSTM_},
                                                      {kOpFormat_FRACTAL_ZN_RNN, FormatMs::FRACTAL_ZN_RNN_},
                                                      {kOpFormat_ND_RNN_BIAS, FormatMs::ND_RNN_BIAS_},
                                                      {kOpFormat_NDC1HWC0, FormatMs::NDC1HWC0_},
                                                      {kOpFormat_NCDHW, FormatMs::NCDHW_},
                                                      {kOpFormat_FRACTAL_Z_3D, FormatMs::FRACTAL_Z_3D_},
                                                      {kOpFormat_DHWNC, FormatMs::DHWNC_},
                                                      {kOpFormat_DHWCN, FormatMs::DHWCN_}};

static const std::string UNKNOWN_STR_ACME = "UNKNOWN_";
static const std::map<TensorFormat, std::string> MAP_FORMAT_TO_STRING_ACME = {
  {TensorFormat::kFormatNCHW, "NCHW"},
  {TensorFormat::kFormatNHWC, "NHWC"},
  {TensorFormat::kFormatND, "ND"},
  {TensorFormat::kFormatNC1HWC0, "NC1HWC0"},
  {TensorFormat::kFormatFRACTAL_Z, "FRACTAL_Z"},
  {TensorFormat::kFormatNC1HWC0_C04, "NC1HWC0_C04"},
  {TensorFormat::kFormatHWCN, "HWCN"},
  {TensorFormat::kFormatNDHWC, "NDHWC"},
  {TensorFormat::kFormatFRACTAL_NZ, "FRACTAL_NZ"},
  {TensorFormat::kFormatNCDHW, "NCDHW"},
  {TensorFormat::kFormatNDC1HWC0, "NDC1HWC0"},
  {TensorFormat::kFormatFRACTAL_Z_3D, "FRACTAL_Z_3D"},
};
const std::string &GetStrWithFormatAcme(const TensorFormat &format);

static const int UNKNOWN_DTYPE_ACME = 0;
// reference: msprof/analysis/csrc/viewer/database/drafts/number_mapping.cpp
enum TensorDtypeMs : int {
  FLOAT = 0,
  FLOAT16 = 1,
  INT8 = 2,
  INT32 = 3,
  UINT8 = 4,
  INT16 = 6,
  UINT16 = 7,
  UINT32 = 8,
  INT64 = 9,
  UINT64 = 10,
  DOUBLE = 11,
  BOOL = 12,
  STRING = 13,
  DUAL_SUB_INT8 = 14,
  DUAL_SUB_UINT8 = 15,
  COMPLEX64 = 16,
  COMPLEX128 = 17,
  QINT8 = 18,
  QINT16 = 19,
  QINT32 = 20,
  QUINT8 = 21,
  QUINT16 = 22,
  RESOURCE = 23,
  STRING_REF = 24,
  DUAL = 25,
  DT_VARIANT = 26,
  DT_BF16 = 27,
  UNDEFINED = 28,
  DT_INT4 = 29,
  DT_UINT1 = 30,
  DT_INT2 = 31,
  DT_UINT2 = 32,
  DT_COMPLEX32 = 33,
  DT_MAX = 34,
  NUMBER_TYPE_BEGIN_ = 229,
  BOOL_ = 230,
  INT_ = 231,
  INT8_ = 232,
  INT16_ = 233,
  INT32_ = 234,
  INT64_ = 235,
  UINT_ = 236,
  UINT8_ = 237,
  UINT16_ = 238,
  UINT32_ = 239,
  UINT64_ = 240,
  FLOAT_ = 241,
  FLOAT16_ = 242,
  FLOAT32_ = 243,
  FLOAT64_ = 244,
  COMPLEX_ = 245,
  NUMBER_TYPE_END_ = 246,
};

static const std::map<int, int> MAP_DTYPE_TO_MSDTYPE_ACME = {
  {DataType::kTypeUnknown, TensorDtypeMs::UNDEFINED},   {DataType::kTypeFloat32, TensorDtypeMs::FLOAT32_},
  {DataType::kTypeFloat16, TensorDtypeMs::FLOAT16_},    {DataType::kTypeInt8, TensorDtypeMs::INT8_},
  {DataType::kTypeInt32, TensorDtypeMs::INT32_},        {DataType::kTypeUint8, TensorDtypeMs::UINT8_},
  {DataType::kTypeInt16, TensorDtypeMs::INT16_},        {DataType::kTypeUint16, TensorDtypeMs::UINT16_},
  {DataType::kTypeUint32, TensorDtypeMs::UINT32_},      {DataType::kTypeInt64, TensorDtypeMs::INT64_},
  {DataType::kTypeUint64, TensorDtypeMs::UINT64_},      {DataType::kTypeFloat64, TensorDtypeMs::FLOAT64_},
  {DataType::kTypeBool, TensorDtypeMs::BOOL_},          {DataType::kTypeString, TensorDtypeMs::STRING_REF},
  {DataType::kTypeComplex64, TensorDtypeMs::COMPLEX64}, {DataType::kTypeComplex128, TensorDtypeMs::COMPLEX128},
  {DataType::kTypeBF16, TensorDtypeMs::DT_BF16}};
const int &GetMsDtypeAcme(const DataType &dtype);

struct NodeInfo {
  // dataCnodeName   NodeFullnameScope
  const char *op_name;
  const char *op_fullname;
  // 使用的核数
  uint32_t block_dim;
  uint64_t input_size{0};
  uint64_t output_size{0};
  std::vector<std::vector<int64_t>> shapes;
  std::vector<std::string> data_formats;
  std::vector<uint32_t> data_types;
};
class MsProfHelper {
 public:
  MsProfHelper(const NodeInfo &info) : info_(info) {};
  ~MsProfHelper() = default;

  void InitReportNode();
  void ReportTask();

 private:
  void InitProfTensorData(const size_t index, const uint64_t offset_idx, MsprofTensorInfo *tensor_info);
  void BuildSingleTensorInfo(const uint64_t opName_hash_id, const size_t index, const uint32_t tensor_num,
                             TensorInfoWrapper *tensor_info_wrapper);

  ProfNodeAdditionInfo addition_info_;
  NodeInfo info_;
};
// reference: msprof/analysis/profiling_bean/prof_enum/data_tag.py
enum CannModuleId {
  SLOG,          /**< Slog */
  IDEDD,         /**< IDE daemon device */
  IDEDH,         /**< IDE daemon host */
  HCCL,          /**< HCCL */
  FMK,           /**< Adapter */
  HIAIENGINE,    /**< Matrix */
  DVPP,          /**< DVPP */
  RUNTIME,       /**< Runtime */
  CCE,           /**< CCE */
  HDC,           /**< HDC */
  DRV,           /**< Driver */
  MDCFUSION,     /**< Mdc fusion */
  MDCLOCATION,   /**< Mdc location */
  MDCPERCEPTION, /**< Mdc perception */
  MDCFSM,
  MDCCOMMON,
  MDCMONITOR,
  MDCBSWP,    /**< MDC base software platform */
  MDCDEFAULT, /**< MDC undefine */
  MDCSC,      /**< MDC spatial cognition */
  MDCPNC,
  MLL,      /**< abandon */
  DEVMM,    /**< Dlog memory managent */
  KERNEL,   /**< Kernel */
  LIBMEDIA, /**< Libmedia */
  CCECPU,   /**< aicpu shedule */
  ASCENDDK, /**< AscendDK */
  ROS,      /**< ROS */
  HCCP,
  ROCE,
  TEFUSION,
  PROFILING, /**< Profiling */
  DP,        /**< Data Preprocess */
  APP,       /**< User Application */
  TS,        /**< TS module */
  TSDUMP,    /**< TSDUMP module */
  AICPU,     /**< AICPU module */
  LP,        /**< LP module */
  TDT,       /**< tsdaemon or aicpu shedule */
  FE,
  MD,
  MB,
  ME,
  IMU,
  IMP,
  GE, /**< Fmk */
  MDCFUSA,
  CAMERA,
  ASCENDCL,
  TEEOS,
  ISP,
  SIS,
  HSM,
  DSS,
  PROCMGR,  // Process Manager, Base Platform
  BBOX,
  AIVECTOR,
  TBE,
  FV,
  MDCMAP,
  TUNE,
  HSS, /**< helper */
  FFTS,
  OP,
  UDF,
  HICAID,
  TSYNC,
  AUDIO,
  TPRT,
  ASCENDCKERNEL,
  ASYS,
  ATRACE,
  RTC,
  SYSMONITOR,
  INVLID_MOUDLE_ID  // add new module before INVLID_MOUDLE_ID
};

int32_t AcmeProfCommandHandler(uint32_t type, VOID_PTR data, uint32_t len);
extern bool gAcmeIsProfiling;
static struct AcmeProfRegister {
  AcmeProfRegister() { MsprofRegisterCallback(CannModuleId::ROCE, AcmeProfCommandHandler); }
} acmeProfCommandHandler;
}  // namespace acme
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_SRC_ACME_UTILS_PROFILING_UTIL_H_
