/*
 * Copyright (c) Huawei Technologies Co., Ltd. 2023. All rights reserved.
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
#ifndef LCAL_LCOC_H
#define LCAL_LCOC_H

#include <lcal_comm.h>

namespace Lcal {
enum CoCDataTypeDesc : int {
    COC_DATA_TYPE_UNDEFINED = -1,
    FP16FP16_FP32_FP16 = 0, // 无量化，无反量化
    BF16BF16_FP32_BF16 = 1, // 无量化，无反量化
    INT8INT8_INT32_FP16 = 2, // W8A8，未融合量化，随路反量化
    INT8INT8_INT32_BF16 = 3, // W8A8，未融合量化，aiv反量化
    FP16INT8_INT32_FP16 = 4, // W8A8，融合量化，随路反量化
    BF16INT8_INT32_BF16 = 5, // W8A8，融合量化，aiv反量化
    FP16INT8_FP32_FP16 = 6, // W8A16，融合伪量化，无反量化
    BF16INT8_FP32_BF16 = 7, // W8A16，融合伪量化，无反量化
    FP16INT4_FP32_FP16 = 8, // W4A16，融合伪量化，无反量化
    BF16INT4_FP32_BF16 = 9, // W4A16，融合伪量化，无反量化
    COC_DATA_TYPE_DESC_MAX = 10,
};

struct MatMulInfo {
    int64_t batchSize = 1;
    int64_t m = -1;
    int64_t k = -1;
    int64_t n = -1;
    bool transA = false;
    bool transB = false;
    bool withBias = false;
    bool isInt8 = false;
};

enum QuantGranularity : int {
    QUANT_GRANULARITY_UNDEFINED = -1,
    PER_TENSOR = 0,
    PER_CHANNEL = 1,
    PER_GROUP = 2,
    QUANT_GRANULARITY_MAX = 3,
};

struct QuantInfo {
    QuantGranularity dequantGranularity = QuantGranularity::QUANT_GRANULARITY_UNDEFINED; // 反量化（包括Matmul前置伪量化和后置反量化）粒度
    int32_t dequantGroupSize = -1;

    QuantGranularity quantGranularity = QuantGranularity::QUANT_GRANULARITY_UNDEFINED; // 量化粒度
    int32_t quantGroupSize = -1;
};

struct CoCParamDesc {
    CoCDataTypeDesc dataTypeDesc = FP16FP16_FP32_FP16;
    MatMulInfo mmInfo = {};
    QuantInfo quantInfo = {};
    HcclReduceOp op = HCCL_REDUCE_SUM; // 当前不支持其他值
};

struct CoCTiling {
    int32_t m0 = -1;
    int32_t k0 = -1;
    int32_t n0 = -1;
    int32_t swizzlDirect = -1;
    int32_t swizzlCount = -1;
    int32_t splitK = -1;
    int32_t ubMoveNum = -1;
    int32_t pValue = -1;
    int32_t write2OtherRank = -1;
    int32_t blockDim = -1;
    int32_t withSerialMode = -1;
};

struct CoCInputPkg {
    void *matrixA = nullptr;
    void *matrixB = nullptr;
    void *bias = nullptr;

    void *dequantScale = nullptr; // 反量化参数，当融合了Matmul前置伪量化或后置反量化操作时需要传入
    void *dequantOffset = nullptr; // 可选，若无offset（如对称量化场景），传入空指针即可

    void *quantScale = nullptr; // 量化参数，当融合了量化操作时需要传入
    void *quantOffset = nullptr; // 可选，若无offset（如对称量化场景），传入空指针即可
};

struct CoCOutputPkg{
    void *output = nullptr;
    void *midOutput = nullptr; // 先通信后计算情况下，通信的中间结果
};

class Lcoc {
public:
    explicit Lcoc(LcalComm &comm);
    ~Lcoc();
    int Init(const std::string &uid = "", int maxBuffSize = LCAL_BUFF_BYTES);
    int SetParam(LcalType lcalType, const CoCTiling &tiling, const CoCParamDesc &paramDesc);
    int MTE2Test(CoCInputPkg inputPkg, CoCOutputPkg outputPkg, void *workspace, aclrtStream stream = nullptr);
    int All2AllMatmul(CoCInputPkg inputPkg, CoCOutputPkg outputPkg, void *workspace, aclrtStream stream = nullptr);
    int AllGatherMatmul(CoCInputPkg inputPkg, CoCOutputPkg outputPkg, void *workspace, aclrtStream stream = nullptr);
    int AllGatherMatmulV2(CoCInputPkg inputPkg, CoCOutputPkg outputPkg, void *workspace, aclrtStream stream = nullptr);
    int MatmulReduceScatter(CoCInputPkg inputPkg, CoCOutputPkg outputPkg, void *workspace,
        aclrtStream stream = nullptr);
    int MatmulAllReduce(CoCInputPkg inputPkg, CoCOutputPkg outputPkg, void *workspace, aclrtStream stream = nullptr);
    int PureMatmul(CoCInputPkg inputPkg, CoCOutputPkg outputPkg, void *workspace, aclrtStream stream = nullptr);
    int64_t GetWorkspaceSize();
    LcalComm &GetComm();
    MatMulInfo &GetMatMulInfo();
    int32_t GetEleSize();
    void GetTiling(CoCTiling &tiling);

private:
    bool CheckDataType() const;
    bool InitTiling(const CoCTiling &tiling);
    int LaunchOperator(CoCInputPkg &inputPkg, CoCOutputPkg &outputPkg, void *workspace, aclrtStream stream);
    bool CheckBasic(const CoCInputPkg &inputPkg, const CoCOutputPkg &outputPkg, LcalType lcalType);

private:
    LcalComm &comm_;
    LcalType lcalType_ = LcalType::ALL_REDUCE;
    CoCParamDesc paramDesc_ = {};
    CoCTiling tiling_ = {};
    int rank_ = 0;
    int rankSize_ = 0;
    bool tilingSuccess_ = false;
};

struct WorkspaceDetail {
    int64_t matrixActivationSize{ 0 };
    int64_t matrixWeightSize{ 0 };
    int64_t matrixIntermediateSize{ 0 };
    int64_t formatDequantParamSize{ 0 };

    int64_t GetSize() const
    {
        return matrixActivationSize + matrixWeightSize + matrixIntermediateSize + formatDequantParamSize;
    }
};

WorkspaceDetail GetWorkspaceDetail(CoCDataTypeDesc dataType, const MatMulInfo &mmInfo, const QuantInfo &quantInfo);

void GetLcalTypeByDeterministic(LcalType &lcalType, bool deterministic);
}
#endif // LCAL_LCOC_H
