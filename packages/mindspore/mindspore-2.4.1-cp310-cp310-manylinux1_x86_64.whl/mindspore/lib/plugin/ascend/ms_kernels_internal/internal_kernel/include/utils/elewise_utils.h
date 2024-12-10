#ifndef MS_KERNELS_INTERNAL_KERNEL_UTILS_ELEWISE_UTILS_H_
#define MS_KERNELS_INTERNAL_KERNEL_UTILS_ELEWISE_UTILS_H_
#include <stdint.h>
#include <vector>
#include <functional>
#include "elewise_tiling.h"
#include "include/ms_int_types.h"
#include "include/param/elewise_param.h"
namespace mindspore {
namespace internal {
#define MAX_COMPARE_SHAPE_LEN MAX_ELEWISE_SHAPE_LEN

/* infershape */
int GetBroadcastMode(const int64_t *in_shape0, const int64_t *in_shape1, const size_t ndims, uint32_t *mode);
int BroadcastInferShape(const int64_t *in_shape0, const int64_t *in_shape1, const size_t ndim, int64_t *output_shape);
void MakeUpInputShapes(const size_t origin_inshape0_size, const size_t origin_inshape1_size,
                       const int64_t *origin_inshape0, const int64_t *origin_inshape1, size_t *ndim, int64_t *in_shape0,
                       int64_t *in_shape1);
bool IsScalarTensor(const int64_t *shape, const size_t ndims);

/* elewise tail tiling */
void ElewiseTailCoreTiling(const uint32_t aligned, const uint32_t total_num, uint32_t &avg_block_count,
                           uint32_t &tail_block_count, uint32_t &core_num);
void ElewiseTailUbTiling(const uint32_t aligned_factor, const uint32_t max_factor, const uint32_t total_num,
                         uint32_t &ub_num, uint32_t &ub_loop, uint32_t &ub_tail);
void ElewiseTailTiling(ElewiseTailTilingData *tiling, const uint32_t total_num, const uint32_t aligned_factor = 64,
                       const uint32_t max_ub_factor = 4094);  // (192 * 1024 - 80) / 2 / (8 * 3)
}  // namespace internal
}  // namespace mindspore
#endif  // MS_KERNELS_INTERNAL_KERNEL_UTILS_ELEWISE_UTILS_H_
