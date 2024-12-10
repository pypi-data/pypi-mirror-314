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
#ifndef LCAL_TYPES_H
#define LCAL_TYPES_H

#include <cstdint>
#include <hccl_types.h>
#include <map>
#include <string>

namespace Lcal {
constexpr int LCAL_SUCCESS = 0;
constexpr int LCAL_ERROR_NOT_INITIALIZED = -1;
constexpr int LCAL_ERROR_ASDRT = -2;
constexpr int LCAL_ERROR_PARA_CHECK_FAIL = -3;
constexpr int LCAL_ERROR_INTERNAL = -4;
constexpr int LCAL_ERROR_TIMEOUT = -5;
constexpr int LCCL_ERROR_INIT_HCCL_FAILED = -6;
constexpr int64_t LCAL_INVALID_VALUE = -1;
constexpr int LCAL_BUFF_BYTES = 202 * 1024 * 1024; // shared buffer size
constexpr int LCAL_MAX_RANK_SIZE = 8;

constexpr uint32_t ALIGN_BYTES = 512;

enum class ChipName {
    CHIP_310P3,
    CHIP_910B1,
    CHIP_910B2,
    CHIP_910B3,
    CHIP_910B4,
    RESERVED,
};

enum class PhysicalLink {
    HCCS = 0,
    PCIE = 1,
    RESERVED,
};

// 包含 物理链路、芯片名称 信息。
struct PhysicalInfo {
    ChipName chipName = ChipName::RESERVED;
    PhysicalLink physicalLink = PhysicalLink::RESERVED;
    uint32_t coreNum = 0;
};

enum class LcalType {
    ALL_REDUCE = 1,
    REDUCE_SCATTER = 2,
    ALL_GATHER = 3,
    BROADCAST = 4,
    ALL2ALL = 5,
    PURE_MATMUL = 101,
    MATMUL_ALL_REDUCE = 102,
    MATMUL_REDUCE_SCATTER = 103,
    ALL_GATHER_MATMUL = 104,
    ALL_GATHER_MATMUL_V2 = 105,
    ALL2ALL_MATMUL = 106,
    MATMUL_ALL2ALL = 107,
    MTE2_TEST = 108,
    MATMUL_ALL_REDUCE_DETERMINISTIC = 109,
    MATMUL_REDUCE_SCATTER_DETERMINISTIC = 110,
    LCAL_TYPE_MAX = 111,
};

const std::map<LcalType, std::string> LCAL_TYPE2NAME = {
    { LcalType::ALL_REDUCE, "LcalAllReduce" },
    { LcalType::REDUCE_SCATTER, "LcalReduceScatter" },
    { LcalType::ALL_GATHER, "LcalAllGather" },
    { LcalType::BROADCAST, "LcalBroadcast" },
    { LcalType::ALL2ALL, "LcalAll2All" },
    { LcalType::PURE_MATMUL, "LcalPureMatmul" },
    { LcalType::MATMUL_ALL_REDUCE, "LcalMatmulAllReduce" },
    { LcalType::MATMUL_REDUCE_SCATTER, "LcalMatmulReduceScatter" },
    { LcalType::ALL_GATHER_MATMUL, "LcalAllGatherMatmul" },
    { LcalType::ALL_GATHER_MATMUL_V2, "LcalAllGatherMatmulV2" },
    { LcalType::ALL2ALL_MATMUL, "LcalAll2AllMatmul" },
    { LcalType::MATMUL_ALL2ALL, "LcalMatmulAll2All" },
    { LcalType::MTE2_TEST, "LcalMTE2Test" },
    { LcalType::MATMUL_ALL_REDUCE_DETERMINISTIC, "LcalMatmulAllReduceDeterministic" },
    { LcalType::MATMUL_REDUCE_SCATTER_DETERMINISTIC, "LcalMatmulReduceScatterDeterministic" },
};

const std::map<LcalType, LcalType> NORMAL2DETERMINISTIC = {
    { LcalType::MATMUL_ALL_REDUCE, LcalType::MATMUL_ALL_REDUCE_DETERMINISTIC },
    { LcalType::MATMUL_REDUCE_SCATTER, LcalType::MATMUL_REDUCE_SCATTER_DETERMINISTIC }
};

} // namespace Lcal
#endif // LCAL_TYPES_H
