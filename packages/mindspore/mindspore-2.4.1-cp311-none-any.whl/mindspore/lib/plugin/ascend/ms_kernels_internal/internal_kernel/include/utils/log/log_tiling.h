#ifndef MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_TILING_H_
#define MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_TILING_H_

#include <iostream>
#include "src/utils/elewise_tiling.h"
#include "src/compare/compare_tiling.h"
#include "src/cast/cast_tiling.h"
#include "src/elewise_binary/elewise_binary_tiling.h"
#include "src/elewise_unary/elewise_unary_tiling.h"
#include "src/sub/sub_tiling.h"

namespace mindspore::internal {
static std::ostream &operator<<(std::ostream &os, const CastTilingData &dt) {
  os << ", buffer_num:" << dt.buffer_num;
  os << ", cast_dtype:" << dt.cast_dtype;
  os << ", core_num:" << dt.core_num;
  os << ", avg_block_count:" << dt.avg_block_count;
  os << ", avg_block_ub_num:" << dt.avg_block_ub_num;
  os << ", avg_block_ub_tail:" << dt.avg_block_ub_tail;
  os << ", avg_block_ub_loop:" << dt.avg_block_ub_loop;
  os << ", tail_block_count:" << dt.tail_block_count;
  os << ", tail_block_ub_num:" << dt.tail_block_ub_num;
  os << ", tail_block_ub_tail:" << dt.tail_block_ub_tail;
  os << ", tail_block_ub_loop:" << dt.tail_block_ub_loop;
  return os;
}
static std::ostream &operator<<(std::ostream &os, const ElewiseTailTilingData &dt) {
  os << ", avg_block_count:" << dt.avg_block_count;
  os << ", avg_block_ub_num:" << dt.avg_block_ub_num;
  os << ", avg_block_ub_tail:" << dt.avg_block_ub_tail;
  os << ", avg_block_ub_loop:" << dt.avg_block_ub_loop;
  os << ", tail_block_count:" << dt.tail_block_count;
  os << ", tail_block_ub_num:" << dt.tail_block_ub_num;
  os << ", tail_block_ub_tail:" << dt.tail_block_ub_tail;
  os << ", tail_block_ub_loop:" << dt.tail_block_ub_loop;
  os << ", buffer_num:" << dt.buffer_num;
  os << ", block_dim:" << dt.block_dim;
  return os;
}
static std::ostream &operator<<(std::ostream &os, const CompareTilingData &dt) {
  os << ", input_dtype:" << dt.input_dtype;
  os << ", broadcast_mode:" << dt.broadcast_mode;
  os << ", compare_mode:" << dt.compare_mode;
  ElewiseTailTilingData *ele_tiling = (ElewiseTailTilingData *)&dt;
  os << *ele_tiling;
  return os;
}

static std::ostream &operator<<(std::ostream &os, const ElewiseBinaryTilingData &dt) {
  os << "broadcast_mode:" << dt.broadcast_mode_;
  os << ", op_dtype:" << dt.op_dtype_;
  ElewiseTailTilingData *ele_tiling = (ElewiseTailTilingData *)&dt;
  os << *ele_tiling;
  return os;
}

static std::ostream &operator<<(std::ostream &os, const ElewiseUnaryTilingData &dt) {
  os << "op_dtype:" << dt.op_dtype_;
  ElewiseTailTilingData *ele_tiling = (ElewiseTailTilingData *)&dt;
  os << *ele_tiling;
  return os;
}
static std::ostream &operator<<(std::ostream &os, const SubTilingData &dt) {
  os << ", broadcast_mode_:" << dt.broadcast_mode_;
  os << ", input_dtype_:" << dt.input_dtype_;
  ElewiseTailTilingData *ele_tiling = (ElewiseTailTilingData *)&dt;
  os << *ele_tiling;
  return os;
}
}  // namespace mindspore::internal
#endif  // MS_KERNELS_INTERNAL_KERNEL_UTILS_LOG_LOG_TILING_H_
