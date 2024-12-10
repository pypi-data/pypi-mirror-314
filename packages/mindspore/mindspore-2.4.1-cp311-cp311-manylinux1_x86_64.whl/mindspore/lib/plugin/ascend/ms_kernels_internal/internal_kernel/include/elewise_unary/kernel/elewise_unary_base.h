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

#ifndef MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_ELEWISE_BASE_H_
#define MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_ELEWISE_BASE_H_

#include "kernel_operator.h"
using namespace AscendC;

template <typename IN_TYPE>
class ElewiseBaseWide {
 public:
  __aicore__ inline ElewiseBaseWide(){};

  __aicore__ inline void InitUnary(GM_ADDR in, GM_ADDR out, GM_ADDR tiling) {
    gm_in1 = reinterpret_cast<__gm__ IN_TYPE *>(in);
    gm_out = reinterpret_cast<__gm__ IN_TYPE *>(out);
    SetTilingInfo(tiling);
  }

  __aicore__ inline void ProcessUnary() { CalculateUnary(); }

  __aicore__ inline void SetUnaryFunc(void (*func)(const LocalTensor<IN_TYPE> &dstLocal,
                                                   const LocalTensor<IN_TYPE> &srcLocal, const int &calCount)) {
    elewise_unary_func_ = func;
  }

 private:
  __aicore__ inline void SetTilingInfo(GM_ADDR tiling) {
    core_idx = get_block_idx();
    core_num = get_block_num();

    avg_block_count = (uint32_t)(*((__gm__ uint32_t *)tiling + 0));
    avg_block_ub_num = (uint32_t)(*((__gm__ uint32_t *)tiling + 1));
    avg_block_ub_tail = (uint32_t)(*((__gm__ uint32_t *)tiling + 2));
    avg_block_ub_loop = (uint32_t)(*((__gm__ uint32_t *)tiling + 3));
    tail_block_count = (uint32_t)(*((__gm__ uint32_t *)tiling + 4));
    tail_block_ub_num = (uint32_t)(*((__gm__ uint32_t *)tiling + 5));
    tail_block_ub_tail = (uint32_t)(*((__gm__ uint32_t *)tiling + 6));
    tail_block_ub_loop = (uint32_t)(*((__gm__ uint32_t *)tiling + 7));

    buffer_num = (uint32_t)(*((__gm__ uint32_t *)tiling + 8));
  }
  __aicore__ inline void SetUbParam(uint32_t &ub_count, uint32_t &ub_loop, uint32_t &ub_tail) {
    ub_count = avg_block_ub_num;
    ub_loop = avg_block_ub_loop;
    ub_tail = avg_block_ub_tail;

    if (core_idx == core_num - 1) {
      ub_count = tail_block_ub_num;
      ub_loop = tail_block_ub_loop;
      ub_tail = tail_block_ub_tail;
    }
  }

  __aicore__ inline void InitUnaryInOut(uint32_t count) {
    pipe.InitBuffer(in1Que, buffer_num, count * sizeof(IN_TYPE));
    pipe.InitBuffer(outQue, buffer_num, count * sizeof(IN_TYPE));
  }

  __aicore__ inline void CopyOut(uint32_t idx, uint32_t stride, uint32_t count) {
    LocalTensor<IN_TYPE> out = outQue.DeQue<IN_TYPE>();
    DataCopy(outGm[idx * stride], out, count);
    outQue.FreeTensor(out);
  }

  __aicore__ inline void CopyIn1(uint32_t idx, uint32_t stride, uint32_t count) {
    LocalTensor<IN_TYPE> in1 = in1Que.AllocTensor<IN_TYPE>();
    DataCopy(in1, in1Gm[idx * stride], count);
    in1Que.EnQue(in1);
  }

  __aicore__ inline void CalculateUnary() {
    uint32_t ub_count, ub_loop, ub_tail;
    SetUbParam(ub_count, ub_loop, ub_tail);

    in1Gm.SetGlobalBuffer(gm_in1 + core_idx * avg_block_count);
    outGm.SetGlobalBuffer(gm_out + core_idx * avg_block_count);

    InitUnaryInOut(ub_count);

    uint32_t loop = 0;
    for (; loop < ub_loop - 1; loop++) {
      CopyIn1(loop, ub_count, ub_count);
      ComputeUnary(ub_count);
      CopyOut(loop, ub_count, ub_count);
    }

    /* for ub tail */
    if (ub_tail <= 0) {
      return;
    }
    CopyIn1(loop, ub_count, ub_tail);
    ComputeUnary(ub_tail);
    CopyOut(loop, ub_count, ub_tail);
  }

  __aicore__ inline void ComputeUnary(uint32_t count) {
    LocalTensor<IN_TYPE> in1 = in1Que.DeQue<IN_TYPE>();
    LocalTensor<IN_TYPE> out = outQue.AllocTensor<IN_TYPE>();
    elewise_unary_func_(out, in1, count);
    in1Que.FreeTensor(in1);
    outQue.EnQue(out);
  }

 private:
  void (*elewise_unary_func_)(const LocalTensor<IN_TYPE> &dstLocal, const LocalTensor<IN_TYPE> &srcLocal,
                              const int &calCount);

  TPipe pipe;
  TQue<AscendC::QuePosition::VECIN, 1> in1Que;
  TQue<AscendC::QuePosition::VECOUT, 1> outQue;

  __gm__ IN_TYPE *__restrict__ gm_in1{nullptr};
  __gm__ IN_TYPE *__restrict__ gm_out{nullptr};

  GlobalTensor<IN_TYPE> in1Gm;
  GlobalTensor<IN_TYPE> outGm;

  uint32_t core_idx{0};
  uint32_t core_num{0};
  uint32_t buffer_num{0};

  uint32_t avg_block_count{0};
  uint32_t avg_block_ub_num{0};
  uint32_t avg_block_ub_tail{0};
  uint32_t avg_block_ub_loop{0};

  uint32_t tail_block_count{0};
  uint32_t tail_block_ub_num{0};
  uint32_t tail_block_ub_tail{0};
  uint32_t tail_block_ub_loop{0};
};

#endif  // MS_KERNELS_INTERNAL_KERNEL_ASCENDC_ELEWISE_ELEWISE_BASE_H_
