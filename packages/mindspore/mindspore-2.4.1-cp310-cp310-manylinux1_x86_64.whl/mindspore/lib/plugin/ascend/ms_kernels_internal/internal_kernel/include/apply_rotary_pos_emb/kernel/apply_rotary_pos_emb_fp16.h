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
#ifndef ROTARY_POS_EMB_FP16
#define ROTARY_POS_EMB_FP16
#include "apply_rotary_pos_emb_fp.h"

using AscendC::HardEvent;

template <typename QK_DTYPE, typename COS_DTYPE, bool IF_COS_BROADCAST>
class RopeFp16 : public Rope<QK_DTYPE, COS_DTYPE, IF_COS_BROADCAST> {
 public:
  __aicore__ inline RopeFp16(RopeTilingData *tilingData, AscendC::TPipe *pipe)
      : Rope<QK_DTYPE, COS_DTYPE, IF_COS_BROADCAST>(tilingData, pipe) {
    this->repeatSize_ = 128;  // 128 = 256B / sizeof(half)
    this->maxProcessNum_ = this->tilingData_->maxUbSize / sizeof(uint16_t);
    this->repeatTimesQ_ = (this->tilingData_->hiddenSizeQ + this->repeatSize_ - 1) / this->repeatSize_;
    this->repeatTimesK_ = (this->tilingData_->hiddenSizeK + this->repeatSize_ - 1) / this->repeatSize_;
    headDimAlign_ = ((this->tilingData_->headDim + ELE_NUM_FP16 - 1) / ELE_NUM_FP16) * ELE_NUM_FP16;
    this->alignHalfHeadDim_ = (this->rotateStride_ * NUM_TWO) % ELE_NUM_FP16;
    this->hiddenSizeAlign_ = ((this->hiddenSize_ + this->repeatSize_ - 1) / this->repeatSize_) * this->repeatSize_;

    this->cosPad_ = 0;
    this->sinPad_ = this->cosPad_ + this->hiddenSizeAlign_;
    this->negOne_ = this->sinPad_ + this->hiddenSizeAlign_;
    this->oriPos_ = this->negOne_ + this->hiddenSizeAlign_;
    this->padBefore_ = this->oriPos_ + this->hiddenSizeAlign_;
    this->removeBefore_ = this->padBefore_ + this->hiddenSizeAlign_;
    sinResPos_ = this->removeBefore_ + this->hiddenSizeAlign_;
    this->repeatTimes_ = this->hiddenSizeAlign_ / this->repeatSize_;

    this->syncOffset_ =
      (this->tilingData_->headDim % ELE_NUM_FP16 == 0) ? this->hiddenSizeAlign_ : this->headNum_ * headDimAlign_;
    this->offsetExtraGm_ = NUM_TWO * this->blockIdx_ * this->syncOffset_;
    this->pipe_->InitBuffer(outQueueCO2_, ((this->maxProcessNum_ - this->batchSize_ * NUM_TWO) * sizeof(QK_DTYPE)));
  }

  __aicore__ inline void Process(__gm__ uint8_t *extra) {
    AscendC::GlobalTensor<uint8_t> extraGm;
    extraGm.SetGlobalBuffer((__gm__ uint8_t *)extra);

    AscendC::LocalTensor<QK_DTYPE> commonUbuf_ = outQueueCO2_.Get<QK_DTYPE>();

    if (this->tilingData_->cosFormat == 1) {
      AscendC::GlobalTensor<COS_DTYPE> extraGmCosDtype;
      extraGmCosDtype.SetGlobalBuffer((__gm__ COS_DTYPE *)extra);
      AscendC::PipeBarrier<PIPE_ALL>();
      this->ExpandCosSin(commonUbuf_, this->cosGm_, extraGmCosDtype);
      this->cosGm_ = extraGmCosDtype;
      AscendC::PipeBarrier<PIPE_ALL>();
      this->ExpandCosSin(commonUbuf_, this->sinGm_,
                         extraGmCosDtype[this->tilingData_->ntokens * this->tilingData_->headDim]);
      this->sinGm_ = extraGmCosDtype[this->tilingData_->ntokens * this->tilingData_->headDim];
      extraGm =
        extraGm[this->tilingData_->ntokens * this->tilingData_->headDim * 4];  // sizeof(uint8_t) * 2 = sizeof(half)
      AscendC::PipeBarrier<PIPE_ALL>();
    }

    this->ExpandNeg(commonUbuf_, sinResPos_, this->headNum_, this->repeatTimes_);  // 根据是否对齐选择1 -1 還是 -1 0
    for (uint32_t zz = 0; zz < this->dynamicRound_; ++zz) {
      this->CosSinBroadcast(extraGm, zz, commonUbuf_, this->tilingData_->hiddenSizeQ);  // cos sin 和 QK 无关

      this->QkComm(this->qGm_[this->blockIdx_ * this->nlCoreRun_ * this->tilingData_->hiddenSizeQ +
                              zz * this->tilingData_->hiddenSizeQ],
                   extraGm, this->tilingData_->hiddenSizeQ, commonUbuf_, this->tilingData_->headNumQ);

      if (this->alignRotary_ == 0) {
        AscendC::PipeBarrier<PIPE_V>();
        this->CalcRopeAlign(commonUbuf_, this->repeatTimesQ_, this->oriPos_, this->removeBefore_, this->padBefore_);
      } else {
        AscendC::SetFlag<HardEvent::MTE2_V>(EVENT_ID1);
        AscendC::WaitFlag<HardEvent::MTE2_V>(EVENT_ID1);
        this->CalcRope(commonUbuf_, this->repeatTimesQ_, this->oriPos_, this->removeBefore_, this->padBefore_,
                       sinResPos_, this->padBefore_);
      }
      AscendC::PipeBarrier<PIPE_ALL>();  // 需要
      DataCopy(this->outQGm_[this->blockIdx_ * this->nlCoreRun_ * this->tilingData_->hiddenSizeQ +
                             zz * this->tilingData_->hiddenSizeQ],
               commonUbuf_[this->padBefore_],
               {1, static_cast<uint16_t>(this->tilingData_->hiddenSizeQ / ELE_NUM_FP16), 0, 0});

      AscendC::SetFlag<HardEvent::MTE3_MTE2>(EVENT_ID1);
      AscendC::WaitFlag<HardEvent::MTE3_MTE2>(EVENT_ID1);

      this->QkComm(this->kGm_[this->blockIdx_ * this->nlCoreRun_ * this->tilingData_->hiddenSizeK +
                              zz * this->tilingData_->hiddenSizeK],
                   extraGm, this->tilingData_->hiddenSizeK, commonUbuf_, this->tilingData_->headNumK);

      if (this->alignRotary_ == 0) {
        AscendC::PipeBarrier<PIPE_V>();
        this->CalcRopeAlign(commonUbuf_, this->repeatTimesK_, this->oriPos_, this->removeBefore_, this->padBefore_);
      } else {
        AscendC::SetFlag<HardEvent::MTE2_V>(EVENT_ID1);
        AscendC::WaitFlag<HardEvent::MTE2_V>(EVENT_ID1);
        this->CalcRope(commonUbuf_, this->repeatTimesK_, this->oriPos_, this->removeBefore_, this->padBefore_,
                       sinResPos_, this->padBefore_);
      }
      AscendC::PipeBarrier<PIPE_ALL>();  // 需要
      DataCopy(this->outKGm_[this->blockIdx_ * this->nlCoreRun_ * this->tilingData_->hiddenSizeK +
                             zz * this->tilingData_->hiddenSizeK],
               commonUbuf_[this->padBefore_],
               {1, static_cast<uint16_t>(this->tilingData_->hiddenSizeK / ELE_NUM_FP16), 0, 0});
      AscendC::SetFlag<HardEvent::MTE3_V>(EVENT_ID1);
      AscendC::WaitFlag<HardEvent::MTE3_V>(EVENT_ID1);
    }
  }

 private:
  AscendC::TBuf<AscendC::TPosition::VECCALC> outQueueCO2_;
  uint32_t headDimAlign_;  // 对齐的headDim
  uint32_t sinResPos_{0};  // fp32的buf中0 0 0 1 1 1的位置
};

#endif