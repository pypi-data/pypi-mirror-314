#ifndef OP_PROTO_H_
#define OP_PROTO_H_

#include "graph/operator_reg.h"
#include "register/op_impl_registry.h"

namespace ge {

REG_OP(AllFinite)
    .INPUT(gradient, ge::TensorType::ALL())
    .OUTPUT(is_finite, ge::TensorType::ALL())
    .OP_END_FACTORY_REG(AllFinite);

REG_OP(DecoderKvCache)
    .INPUT(cache, ge::TensorType::ALL())
    .INPUT(update, ge::TensorType::ALL())
    .INPUT(valid_seq_len, ge::TensorType::ALL())
    .INPUT(batch_index, ge::TensorType::ALL())
    .INPUT(seq_len_axis, ge::TensorType::ALL())
    .INPUT(new_max_seq_len, ge::TensorType::ALL())
    .INPUT(cur_max_seq_len, ge::TensorType::ALL())
    .OUTPUT(out, ge::TensorType::ALL())
    .OP_END_FACTORY_REG(DecoderKvCache);

REG_OP(PromptKvCache)
    .INPUT(cache, ge::TensorType::ALL())
    .INPUT(update, ge::TensorType::ALL())
    .INPUT(valid_seq_len, ge::TensorType::ALL())
    .INPUT(batch_index, ge::TensorType::ALL())
    .INPUT(seq_len_axis, ge::TensorType::ALL())
    .INPUT(new_max_seq_len, ge::TensorType::ALL())
    .INPUT(cur_max_seq_len, ge::TensorType::ALL())
    .OUTPUT(out, ge::TensorType::ALL())
    .OP_END_FACTORY_REG(PromptKvCache);

}

#endif
