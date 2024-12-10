#ifndef MS_KERNELS_INTERNAL_KERNEL_UTILS_ELEWISE_TILINT_H_
#define MS_KERNELS_INTERNAL_KERNEL_UTILS_ELEWISE_TILINT_H_
#include <stdint.h>
namespace mindspore::internal {
enum BroadcastMode : uint32_t {
  BROADCAST_NONE = 0,     /* in1 == in2 */
  BROADCAST_LEFT,         /* in1 != in2  && in2 == out */
  BROADCAST_RIGHT,        /* in1 != in2  && in1 == out */
  BROADCAST_SCALAR_LEFT,  /* in1 != in2  && in1 == 1 */
  BROADCAST_SCALAR_RIGHT, /* in1 != in2  && in2 == 1 */
  BROADCAST_BOTH,         /* in1 != in2  && in1 != out && in2 != out */
  UNKNOW_BROADCAST_MODE
};
struct ElewiseTailTilingData {
  uint32_t avg_block_count{0};
  uint32_t avg_block_ub_num{0};
  uint32_t avg_block_ub_tail{0};
  uint32_t avg_block_ub_loop{0};

  uint32_t tail_block_count{0};
  uint32_t tail_block_ub_num{0};
  uint32_t tail_block_ub_tail{0};
  uint32_t tail_block_ub_loop{0};

  uint32_t buffer_num{1};
  uint32_t block_dim{1};
};
}  // namespace mindspore::internal
#endif  // MS_KERNELS_INTERNAL_KERNEL_UTILS_ELEWISE_TILINT_H_
