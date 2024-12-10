
/**
 * Copyright (c) Huawei Technologies Co., Ltd. 2024. All rights reserved.
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
#ifndef ROTARY_POS_EMB_BASE
#define ROTARY_POS_EMB_BASE

#include "apply_rotary_pos_emb_tiling.h"
#include "apply_rotary_pos_emb_value.h"
#include "kernel_operator.h"

template <typename QkDtype, typename CosDtype, bool IF_COS_BROADCAST>
class RopeBase {
 public:
  // QkDtype ：输入qk和输出qk的数据类型
  // CosDtype ：输入cos/sin的数据类型
  // IF_COS_BROADCAST ：cos sin是否已扩展
  // 构造函数
  __aicore__ inline RopeBase(RopeTilingData *tilingData) {
    setCtrl_ = get_ctrl();
#if __CCE_AICORE__ == 220
    set_ctrl(sbitset0(get_ctrl(), REG_910B));
#elif __CCE_AICORE__ == 200
    set_ctrl(sbitset1(get_ctrl(), REG_310P));
#endif
    this->tilingData_ = tilingData;
    batchSize_ = (tilingData_->cosFormat == 0)
                   ? 0
                   : ((tilingData_->batch + DEFAULT_REPEAT_STRIDE - 1) / DEFAULT_REPEAT_STRIDE) * DEFAULT_REPEAT_STRIDE;
    hiddenSize_ =
      tilingData_->hiddenSizeK > tilingData_->hiddenSizeQ ? tilingData_->hiddenSizeK : tilingData_->hiddenSizeQ;
    nlCoreRun_ = (tilingData_->ntokens + tilingData_->realCore - 1) / tilingData_->realCore;
    lCoreRun_ = tilingData_->ntokens - (tilingData_->realCore - 1) * nlCoreRun_;
    headNum_ = tilingData_->headNumK > tilingData_->headNumQ ? tilingData_->headNumK : tilingData_->headNumQ;
    rotateStride_ = tilingData_->headDim / tilingData_->rotaryCoeff;
    dynamicRound_ = (block_idx == tilingData_->realCore - 1) ? lCoreRun_ : nlCoreRun_;
    rotaryStrideOffset = (tilingData_->headDim == tilingData_->rotaryCoeff) ? 1 : rotateStride_;
    alignRotary_ = rotateStride_ % ELE_NUM_FP16;
    pipe_.InitBuffer(seqLenQueue_, 1, (batchSize_ * sizeof(int32_t)));
  }

  // 初始化Gm
  __aicore__ inline void RopeInitGm(__gm__ uint8_t *q, __gm__ uint8_t *k, __gm__ uint8_t *cos, __gm__ uint8_t *sin,
                                    __gm__ uint8_t *seqLen, __gm__ uint8_t *outQ, __gm__ uint8_t *outK) {
    qGm_ = (__gm__ QkDtype *)q;
    kGm_ = (__gm__ QkDtype *)k;
    cosGm_ = (__gm__ CosDtype *)cos;
    sinGm_ = (__gm__ CosDtype *)sin;
    outQGm_ = (__gm__ QkDtype *)outQ;
    outKGm_ = (__gm__ QkDtype *)outK;
    seqLenGm_ = (__gm__ uint32_t *)seqLen;
  }

  template <typename T>
  __aicore__ inline void Copy2Ub(__gm__ T *src, __ubuf__ T *dst, uint32_t copyLen) {
#if defined(__CCE_KT_TEST__) || (__CCE_AICORE__ == 220)
    if (g_coreType == AscendC::AIC) return;
#endif
    uint32_t blkSizeReal = BLK_SIZE / sizeof(T);
    if (copyLen % blkSizeReal != 0) {
      copy_gm_to_ubuf(dst, src, 0, 1, (copyLen + blkSizeReal - 1) / blkSizeReal, 0, 0);
      pipe_barrier((PIPE_ALL));
    } else {
      copy_gm_to_ubuf(dst, src, 0, 1, copyLen / blkSizeReal, 0, 0);
      pipe_barrier((PIPE_ALL));
    }
  }

  template <typename T>
  __aicore__ inline void Copy2Gm(__ubuf__ T *src, __gm__ T *dst, uint32_t hiddenSizeLen) {
#if defined(__CCE_KT_TEST__) || (__CCE_AICORE__ == 220)
    if (g_coreType == AscendC::AIC) return;
#endif
    uint32_t blkSizeReal = BLK_SIZE / sizeof(T);
    if (hiddenSizeLen % blkSizeReal != 0) {
      copy_ubuf_to_gm(dst, src, 0, 1, (hiddenSizeLen + blkSizeReal - 1) / blkSizeReal, 0, 0);
    } else {
      copy_ubuf_to_gm(dst, src, 0, 1, hiddenSizeLen / blkSizeReal, 0, 0);
    }
  }

  // 此函数用来复用unpad情況下的cos和sin
  // 例：cos[0~7] cos[0~3]用于第一个batch， cos[0~4]用于第二个batch
  __aicore__ inline void ExpandCosSin(__ubuf__ CosDtype *tempBuf, __gm__ CosDtype *src, __gm__ CosDtype *extraGm) {
#if defined(__CCE_KT_TEST__) || (__CCE_AICORE__ == 220)
    if (g_coreType == AscendC::AIC) return;
#endif
    // cos or sin,[maxseqlen,headsize]-->[sumseqlen,hiddensize]
    AscendC::LocalTensor<int32_t> seqLenLocal = seqLenQueue_.AllocTensor<int32_t>();
    copy_gm_to_ubuf((__ubuf__ int32_t *)seqLenLocal.GetPhyAddr(), seqLenGm_, 0, 1,
        batchSize_ * sizeof(int32_t) / 32, 0, 0);
    pipe_barrier((PIPE_ALL));
    int32_t rowsPerLoop = (maxProcessNum_ - batchSize_ * NUM_TWO) / tilingData_->headDim;
    int32_t cosoffset = 0;
    for (uint32_t perBatch = 0; perBatch < tilingData_->batch; perBatch++) {
      int32_t rowsRepeat = seqLenLocal.GetValue(perBatch) / rowsPerLoop;
      int32_t rowsRemain = seqLenLocal.GetValue(perBatch) % rowsPerLoop;
      for (int32_t j = 0; j < rowsRepeat; j++) {
        Copy2Ub(src + (j * rowsPerLoop) * tilingData_->headDim, tempBuf, rowsPerLoop * tilingData_->headDim);
        Copy2Gm(tempBuf, (extraGm + (cosoffset + j * rowsPerLoop) * tilingData_->headDim),
                rowsPerLoop * tilingData_->headDim);
        pipe_barrier((PIPE_ALL));
      }
      if (rowsRemain > 0) {
        Copy2Ub(src + (rowsRepeat * rowsPerLoop) * tilingData_->headDim, tempBuf, rowsRemain * tilingData_->headDim);
        Copy2Gm(tempBuf, (extraGm + (cosoffset + rowsRepeat * rowsPerLoop) * tilingData_->headDim),
                rowsRemain * tilingData_->headDim);
        pipe_barrier((PIPE_ALL));
      }
      cosoffset += seqLenLocal.GetValue(perBatch);
    }
    seqLenQueue_.FreeTensor(seqLenLocal);
    pipe_barrier((PIPE_ALL));
  }

  // 构建tensor -1 -1 -1 0 0 0
  // 构建tensor 0 0 0 1 1 1
  template <typename BUF_TYPE>
  __aicore__ inline void ExpandNeg(__ubuf__ BUF_TYPE *tempBuf, uint32_t bufPos, uint32_t headNumTemp,
                                   uint32_t repeatTimeTemp) {
    if (tilingData_->headDim != tilingData_->rotaryCoeff) {
      if (alignRotary_ == 0) {  // 对齐直接 -1 1
        for (uint32_t i = 0; i < rotateStride_; ++i) {
          *(tempBuf + negOne_ + i) = (BUF_TYPE)-1;
          *(tempBuf + negOne_ + i + rotateStride_) = (BUF_TYPE)1;
        }
        set_flag(PIPE_S, PIPE_V, EVENT_ID1);
        wait_flag(PIPE_S, PIPE_V, EVENT_ID1);
        for (uint32_t i = 1; i < headNumTemp * tilingData_->rotaryCoeff / NUM_TWO; ++i) {
          // halfHeadDim = rotateStride_ * 2
          copy_ubuf_to_ubuf(tempBuf + negOne_ + rotateStride_ * NUM_TWO * i, tempBuf + negOne_, 0, 1,
                            rotateStride_ * sizeof(BUF_TYPE) / ELE_NUM_FP16, 0, 0);
        }
      } else {
        for (uint32_t i = 0; i < rotateStride_; ++i) {  // 非对齐 -1 0
          *(tempBuf + negOne_ + i) = (BUF_TYPE)-1;
          *(tempBuf + negOne_ + i + rotateStride_) = (BUF_TYPE)0;
        }
        set_flag(PIPE_S, PIPE_V, EVENT_ID1);
        wait_flag(PIPE_S, PIPE_V, EVENT_ID1);
        for (uint32_t i = 0; i < headNumTemp * tilingData_->rotaryCoeff / NUM_TWO; ++i) {
          if ((rotateStride_ * NUM_TWO) * sizeof(BUF_TYPE) % BLK_SIZE == 0) {
            copy_ubuf_to_ubuf(tempBuf + negOne_ + rotateStride_ * NUM_TWO * i, tempBuf + negOne_, 0, 1,
                              rotateStride_ * NUM_TWO * sizeof(BUF_TYPE) / ELE_NUM_FP16, 0, 0);
          } else {
            for (uint32_t j = 0; j < rotateStride_ * NUM_TWO; j++) {
              *(tempBuf + negOne_ + rotateStride_ * NUM_TWO * i + j) = *(tempBuf + negOne_ + j);
            }
          }
        }
        set_flag(PIPE_S, PIPE_V, EVENT_ID1);
        wait_flag(PIPE_S, PIPE_V, EVENT_ID1);
        pipe_barrier(PIPE_V);
        vadds(tempBuf + bufPos, tempBuf + negOne_, (BUF_TYPE)1, repeatTimeTemp, 1, 1, DEFAULT_REPEAT_STRIDE,
              DEFAULT_REPEAT_STRIDE);
      }
    } else {
      set_vector_mask((uint64_t)-1, (uint64_t)-1);
      vector_dup(tempBuf + negOne_, (BUF_TYPE)-1.0, repeatTimeTemp, 1, 1, (uint16_t)DEFAULT_REPEAT_STRIDE,
                 (uint16_t)DEFAULT_REPEAT_STRIDE);
      set_vector_mask(0xaaaaaaaaaaaaaaaa, 0xaaaaaaaaaaaaaaaa);
      vector_dup(tempBuf + negOne_, (BUF_TYPE)0.0, repeatTimeTemp, 1, 1, (uint16_t)DEFAULT_REPEAT_STRIDE,
                 (uint16_t)DEFAULT_REPEAT_STRIDE);
      set_vector_mask((uint64_t)-1, (uint64_t)-1);
      pipe_barrier((PIPE_V));
      vadds(tempBuf + bufPos, tempBuf + negOne_, (BUF_TYPE)1, repeatTimeTemp, 1, 1, DEFAULT_REPEAT_STRIDE,
            DEFAULT_REPEAT_STRIDE);
    }
  }

  // 从(tilingData_->headDim)->(heads*tilingData_->headDim)
  __aicore__ inline void CosSinCommonBroardcast(__gm__ uint8_t *extraGm, uint32_t z, __ubuf__ CosDtype *tempBuf,
                                                uint32_t calcLen) {
    // 永远的先拷一次
    uint32_t cosOffset = block_idx * nlCoreRun_ * tilingData_->headDim + z * tilingData_->headDim;
    uint32_t sinOffset = block_idx * nlCoreRun_ * tilingData_->headDim + z * tilingData_->headDim;
    set_flag(PIPE_S, PIPE_MTE2, EVENT_ID1);
    wait_flag(PIPE_S, PIPE_MTE2, EVENT_ID1);
    copy_gm_to_ubuf(tempBuf + cosPad_, cosGm_ + cosOffset, 0, 1,
                    (tilingData_->headDim * sizeof(CosDtype) + BLK_SIZE - 1) / BLK_SIZE, 0, 0);
    copy_gm_to_ubuf(tempBuf + sinPad_, sinGm_ + sinOffset, 0, 1,
                    (tilingData_->headDim * sizeof(CosDtype) + BLK_SIZE - 1) / BLK_SIZE, 0, 0);
    if (tilingData_->cosFormat == 1) {
      pipe_barrier(PIPE_ALL);
    }
    set_flag(PIPE_MTE2, PIPE_MTE3, EVENT_ID3);
    set_flag(PIPE_MTE2, PIPE_V, EVENT_ID3);
    if ((tilingData_->headDim * sizeof(CosDtype)) % BLK_SIZE != 0) {
      wait_flag(PIPE_MTE2, PIPE_MTE3, EVENT_ID3);
      // 补齐cos，从(tilingData_->headDim)->(heads*tilingData_->headDim)
      // headnum
      for (uint32_t i = 0; i < calcLen / tilingData_->headDim; ++i) {
        copy_ubuf_to_gm((__gm__ CosDtype *)extraGm + offsetExtraGm_ + tilingData_->headDim * i, tempBuf + cosPad_, 0, 1,
                        (tilingData_->headDim * sizeof(CosDtype) + BLK_SIZE - 1) / BLK_SIZE, 0, 0);
        pipe_barrier((PIPE_ALL));
      }
      Copy2Ub<CosDtype>((__gm__ CosDtype *)extraGm + offsetExtraGm_, tempBuf + cosPad_, calcLen);
      // 补齐sin，从(tilingData_->headDim)->(heads*tilingData_->headDim)
      for (uint32_t i = 0; i < calcLen / tilingData_->headDim; ++i) {
        copy_ubuf_to_gm((__gm__ CosDtype *)extraGm + offsetExtraGm_ + tilingData_->headDim * i, tempBuf + sinPad_, 0, 1,
                        (tilingData_->headDim * sizeof(CosDtype) + BLK_SIZE - 1) / BLK_SIZE, 0, 0);
        pipe_barrier((PIPE_ALL));
      }
      Copy2Ub<CosDtype>((__gm__ CosDtype *)extraGm + offsetExtraGm_, tempBuf + sinPad_, calcLen);
      wait_flag(PIPE_MTE2, PIPE_V, EVENT_ID3);
    } else {
      wait_flag(PIPE_MTE2, PIPE_V, EVENT_ID3);
      for (uint32_t i = 1; i < calcLen / tilingData_->headDim; ++i) {
        copy_ubuf_to_ubuf(tempBuf + cosPad_ + tilingData_->headDim * i, tempBuf + cosPad_, 0, 1,
                          tilingData_->headDim * sizeof(CosDtype) / BLK_SIZE, 0, 0);
        copy_ubuf_to_ubuf(tempBuf + sinPad_ + tilingData_->headDim * i, tempBuf + sinPad_, 0, 1,
                          tilingData_->headDim * sizeof(CosDtype) / BLK_SIZE, 0, 0);
      }
      wait_flag(PIPE_MTE2, PIPE_MTE3, EVENT_ID3);
    }
  }

  // 满足 cos sin 多头输入
  template <typename BUF_TYPE>
  __aicore__ inline void CosSinBroadcast(__gm__ uint8_t *extraGm, uint32_t z, __ubuf__ BUF_TYPE *tempBuf,
                                         uint32_t Calclen) {
    if constexpr (IF_COS_BROADCAST) {
      copy_gm_to_ubuf(tempBuf + cosPad_,
                      cosGm_ + block_idx * nlCoreRun_ * tilingData_->hiddenSizeQ + z * tilingData_->hiddenSizeQ, 0, 1,
                      Calclen * sizeof(BUF_TYPE) / BLK_SIZE, 0, 0);
      copy_gm_to_ubuf(tempBuf + sinPad_,
                      sinGm_ + block_idx * nlCoreRun_ * tilingData_->hiddenSizeQ + z * tilingData_->hiddenSizeQ, 0, 1,
                      Calclen * sizeof(BUF_TYPE) / BLK_SIZE, 0, 0);
    } else {
      CosSinCommonBroardcast(extraGm, z, tempBuf, Calclen);
    }
  }

  // qk 公用函数
  template <typename BUF_TYPE>
  __aicore__ inline void QkComm(__gm__ BUF_TYPE *src, __gm__ uint8_t *extraGm1, uint32_t hiddenSizeTmp,
                                __ubuf__ BUF_TYPE *tempBuf, uint32_t headNumTemp) {
    uint32_t hiddenSizeBlk = hiddenSizeTmp / ELE_NUM_FP16;
    set_flag(PIPE_S, PIPE_MTE2, EVENT_ID1);
    wait_flag(PIPE_S, PIPE_MTE2, EVENT_ID1);
    copy_gm_to_ubuf(tempBuf + oriPos_,  // gm -> ub
                    src, 0, 1, hiddenSizeBlk, 0, 0);
    set_flag(PIPE_MTE2, PIPE_V, EVENT_ID1);
    set_flag(PIPE_MTE2, PIPE_MTE3, EVENT_ID2);
    if (alignRotary_ == 0) {
      wait_flag(PIPE_MTE2, PIPE_V, EVENT_ID1);
      wait_flag(PIPE_MTE2, PIPE_MTE3, EVENT_ID2);
      copy_ubuf_to_ubuf(tempBuf + removeBefore_ + rotaryStrideOffset, tempBuf + oriPos_, 0,
                        headNumTemp * tilingData_->rotaryCoeff / 2, rotaryStrideOffset / ELE_NUM_FP16,
                        rotaryStrideOffset / ELE_NUM_FP16, rotaryStrideOffset / ELE_NUM_FP16);

      copy_ubuf_to_ubuf(tempBuf + removeBefore_, tempBuf + oriPos_ + rotaryStrideOffset, 0,
                        headNumTemp * tilingData_->rotaryCoeff / 2, rotaryStrideOffset / ELE_NUM_FP16,
                        rotaryStrideOffset / ELE_NUM_FP16, rotaryStrideOffset / ELE_NUM_FP16);
    } else {
      wait_flag(PIPE_MTE2, PIPE_V, EVENT_ID1);
      wait_flag(PIPE_MTE2, PIPE_MTE3, EVENT_ID2);
      // ub -> workspace[0~hiddensize]
      copy_ubuf_to_gm((__gm__ BUF_TYPE *)extraGm1 + offsetExtraGm_, tempBuf + oriPos_, 0, 1, hiddenSizeBlk, 0, 0);
      // ub -> workspace[hiddensize ~ 2 * hiddensize]
      copy_ubuf_to_gm((__gm__ BUF_TYPE *)extraGm1 + offsetExtraGm_ + hiddenSizeTmp, tempBuf + oriPos_, 0, 1,
                      hiddenSizeBlk, 0, 0);
      // workspace[rotary ~ hiddensize + rotary] -> ub[hiddensize ~ 2 * hiddensize]
      pipe_barrier((PIPE_ALL));
      copy_gm_to_ubuf(tempBuf + removeBefore_, (__gm__ BUF_TYPE *)extraGm1 + offsetExtraGm_ + rotateStride_, 0, 1,
                      hiddenSizeBlk, 0, 0);
      // gm[hiddensize - rotary ~ 2 * hiddensize - rotary] -> ub[2 *hiddensize ~ 3 * hiddensize]
      copy_gm_to_ubuf(tempBuf + padBefore_,
                      (__gm__ BUF_TYPE *)extraGm1 + offsetExtraGm_ + hiddenSizeTmp - rotateStride_, 0, 1, hiddenSizeBlk,
                      0, 0);
    }
  }

  // 主体计算逻辑
  template <typename BUF_TYPE>
  __aicore__ inline void CalcRope(__ubuf__ BUF_TYPE *tempBuf, uint32_t repeatTimes1, uint32_t oriPosTemp,
                                  uint32_t removeTemp, uint32_t padTemp, uint32_t posTemp, uint32_t res) {
    set_vector_mask((uint64_t)-1, (uint64_t)-1);
#if defined(__CCE_KT_TEST__) || (__CCE_AICORE__ == 220)
    if (g_coreType == AscendC::AIC) return;
#endif

    vmul(tempBuf + oriPosTemp, tempBuf + cosPad_, tempBuf + oriPosTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    vmul(tempBuf + padTemp, tempBuf + posTemp, tempBuf + padTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    pipe_barrier((PIPE_V));
    vmul(tempBuf + removeTemp, tempBuf + sinPad_, tempBuf + removeTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    vmul(tempBuf + padTemp, tempBuf + sinPad_, tempBuf + padTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    pipe_barrier((PIPE_V));

    vmul(tempBuf + removeTemp, tempBuf + negOne_, tempBuf + removeTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    vadd(tempBuf + padTemp, tempBuf + oriPosTemp, tempBuf + padTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    pipe_barrier((PIPE_V));

    vadd(tempBuf + res, tempBuf + removeTemp, tempBuf + padTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    pipe_barrier((PIPE_V));
    set_ctrl(setCtrl_);
  }

  // 主体计算逻辑
  template <typename BUF_TYPE>
  __aicore__ inline void CalcRopeAlign(__ubuf__ BUF_TYPE *tempBuf, uint32_t repeatTimes1, uint32_t oriPosTemp,
                                       uint32_t removeTemp, uint32_t padTemp) {
    set_vector_mask((uint64_t)-1, (uint64_t)-1);
#if defined(__CCE_KT_TEST__) || (__CCE_AICORE__ == 220)
    if (g_coreType == AscendC::AIC) return;
#endif
    vmul(tempBuf + oriPosTemp, tempBuf + cosPad_, tempBuf + oriPosTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    vmul(tempBuf + removeTemp, tempBuf + negOne_, tempBuf + removeTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    pipe_barrier((PIPE_V));
    vmul(tempBuf + removeTemp, tempBuf + sinPad_, tempBuf + removeTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    pipe_barrier((PIPE_V));
    vadd(tempBuf + padTemp, tempBuf + removeTemp, tempBuf + oriPosTemp,
         repeatTimes1,           // repeat times
         1,                      // dstBlockStride
         1,                      // src0BlockStride
         1,                      // src1BlockStride
         DEFAULT_REPEAT_STRIDE,  // dstRepeatStride
         DEFAULT_REPEAT_STRIDE,  // src0RepeatStride
         DEFAULT_REPEAT_STRIDE   // src1RepeatStride
    );
    pipe_barrier((PIPE_V));
    set_ctrl(setCtrl_);
  }

 public:
  RopeTilingData *tilingData_ = nullptr;
  __gm__ QkDtype *qGm_{nullptr};
  __gm__ QkDtype *kGm_{nullptr};
  __gm__ CosDtype *cosGm_{nullptr};
  __gm__ CosDtype *sinGm_{nullptr};
  __gm__ uint32_t *seqLenGm_{nullptr};
  __gm__ QkDtype *outQGm_{nullptr};
  __gm__ QkDtype *outKGm_{nullptr};
  AscendC::TPipe pipe_;
  AscendC::TQue<AscendC::QuePosition::VECIN, 1> seqLenQueue_;

  uint32_t cosPad_{0};             // broadcast的cos在uB中的位置
  uint32_t sinPad_{0};             // broadcast的sin在uB中的位置
  uint32_t negOne_{0};             // -1 -1 -1 0 0 0在uB中的位置
  uint32_t oriPos_{0};             // q,k在uB中的位置
  uint32_t padBefore_{0};          // 保存qk[-x : hiddensize - x]
  uint32_t removeBefore_{0};       // 保存qk[x : hiddensize + x]
  uint32_t repeatSize_{0};         // 一拍做几个元素
  uint32_t maxProcessNum_{0};      // 最大处理元素个数
  uint32_t repeatTimesQ_{0};       // q重复次数
  uint32_t repeatTimesK_{0};       // k重复次数
  uint32_t hiddenSizeAlign_{0};    // 对齐后的hiddensize
  uint32_t repeatTimes_{0};        // 对齐后重复次数
  uint32_t headNum_{0};            // 几个头
  uint32_t hiddenSize_{0};         // hiddensizeQ,K的最大值
  uint32_t nlCoreRun_{0};          // 非最后一个核需要跑几次
  uint32_t lCoreRun_{0};           // 最后一个核需要跑几次
  uint32_t batchSize_{0};          // batch向上取整
  uint32_t rotateStride_{0};       // headdim / 旋转系数
  uint32_t offsetExtraGm_{0};      // 使用workspace需要的offset
  uint32_t dynamicRound_{0};       // 每个核做几轮
  uint32_t setCtrl_;               // 复位寄存器
  uint32_t alignHalfHeadDim_{0};   // headDim / 旋转系数 * 2 是否对齐
  uint32_t rotaryStrideOffset{0};  // 每次旋转长度
  uint32_t alignRotary_;           // 旋转距离是否对齐
  uint32_t syncOffset_;            // 每个核使用workspace的offset
};

#endif
