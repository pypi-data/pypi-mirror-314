# Copyright 2023 Huawei Technologies Co., Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================

from mindspore.common._stub_tensor import _convert_stub
from mindspore.ops.auto_generate.gen_arg_handler import *
from mindspore._c_expression import ArgMaxWithValuePrim_
from mindspore._c_expression import ArgMinWithValuePrim_
from mindspore._c_expression import BatchMatMulPrim_
from mindspore._c_expression import BatchNormGradExtPrim_
from mindspore._c_expression import BinaryCrossEntropyGradPrim_
from mindspore._c_expression import BinaryCrossEntropyPrim_
from mindspore._c_expression import BCEWithLogitsLossPrim_
from mindspore._c_expression import BroadcastToPrim_
from mindspore._c_expression import ConcatPrim_
from mindspore._c_expression import ConvolutionGradPrim_
from mindspore._c_expression import ConvolutionPrim_
from mindspore._c_expression import CrossPrim_
from mindspore._c_expression import CummaxPrim_
from mindspore._c_expression import EluExtPrim_
from mindspore._c_expression import FFNExtPrim_
from mindspore._c_expression import FlashAttentionScoreGradPrim_
from mindspore._c_expression import FlashAttentionScorePrim_
from mindspore._c_expression import GridSampler2DGradPrim_
from mindspore._c_expression import GridSampler2DPrim_
from mindspore._c_expression import GridSampler3DGradPrim_
from mindspore._c_expression import GridSampler3DPrim_
from mindspore._c_expression import HShrinkGradPrim_
from mindspore._c_expression import HShrinkPrim_
from mindspore._c_expression import IncreFlashAttentionPrim_
from mindspore._c_expression import IsClosePrim_
from mindspore._c_expression import LogSoftmaxGradPrim_
from mindspore._c_expression import LogSoftmaxPrim_
from mindspore._c_expression import MatMulPrim_
from mindspore._c_expression import MaxPoolGradWithIndicesPrim_
from mindspore._c_expression import MaxPoolGradWithMaskPrim_
from mindspore._c_expression import MaxPoolWithIndicesPrim_
from mindspore._c_expression import MaxPoolWithMaskPrim_
from mindspore._c_expression import NanToNumPrim_
from mindspore._c_expression import OneHotExtPrim_
from mindspore._c_expression import ReduceAllPrim_
from mindspore._c_expression import ReduceAnyPrim_
from mindspore._c_expression import ReverseV2Prim_
from mindspore._c_expression import RmsNormPrim_
from mindspore._c_expression import RollPrim_
from mindspore._c_expression import SearchSortedPrim_
from mindspore._c_expression import SoftmaxPrim_
from mindspore._c_expression import SoftShrinkGradPrim_
from mindspore._c_expression import SoftShrinkPrim_
from mindspore._c_expression import StackExtPrim_
from mindspore._c_expression import TrilExtPrim_
from mindspore._c_expression import TriuPrim_
from mindspore._c_expression import UpsampleTrilinear3DGradPrim_
from mindspore._c_expression import UpsampleTrilinear3DPrim_
from mindspore._c_expression import GroupedMatmulPrim_
from mindspore._c_expression import QuantBatchMatmulPrim_
from mindspore._c_expression import WeightQuantBatchMatmulPrim_


class _PyboostArgMaxWithValuePrim(ArgMaxWithValuePrim_):
    def __call__(self, input, axis, keep_dims):

        return _convert_stub(super().__call__(input, axis, keep_dims))


argmax_with_value_impl = _PyboostArgMaxWithValuePrim()


class _PyboostArgMinWithValuePrim(ArgMinWithValuePrim_):
    def __call__(self, input, axis, keep_dims):

        return _convert_stub(super().__call__(input, axis, keep_dims))


argmin_with_value_impl = _PyboostArgMinWithValuePrim()


class _PyboostBatchMatMulPrim(BatchMatMulPrim_):
    def __call__(self, x, y, transpose_a, transpose_b):

        return _convert_stub(super().__call__(x, y, transpose_a, transpose_b))


batch_mat_mul_impl = _PyboostBatchMatMulPrim()


class _PyboostBatchNormGradExtPrim(BatchNormGradExtPrim_):
    def __call__(self, dout, input, weight, running_mean, running_var, saved_mean, saved_rstd, training, eps):

        return _convert_stub(super().__call__(dout, input, weight, running_mean, running_var, saved_mean, saved_rstd, training, eps))


batch_norm_grad_ext_impl = _PyboostBatchNormGradExtPrim()


class _PyboostBinaryCrossEntropyGradPrim(BinaryCrossEntropyGradPrim_):
    def __call__(self, input, target, grad_output, weight, reduction):
        converted_reduction = str_to_enum('binary_cross_entropy_grad', 'reduction', reduction)
        return _convert_stub(super().__call__(input, target, grad_output, weight, converted_reduction))


binary_cross_entropy_grad_impl = _PyboostBinaryCrossEntropyGradPrim()


class _PyboostBinaryCrossEntropyPrim(BinaryCrossEntropyPrim_):
    def __call__(self, input, target, weight, reduction):
        converted_reduction = str_to_enum('binary_cross_entropy', 'reduction', reduction)
        return _convert_stub(super().__call__(input, target, weight, converted_reduction))


binary_cross_entropy_impl = _PyboostBinaryCrossEntropyPrim()


class _PyboostBCEWithLogitsLossPrim(BCEWithLogitsLossPrim_):
    def __call__(self, input, target, weight, posWeight, reduction):
        converted_reduction = str_to_enum('binary_cross_entropy_with_logits', 'reduction', reduction)
        return _convert_stub(super().__call__(input, target, weight, posWeight, converted_reduction))


binary_cross_entropy_with_logits_impl = _PyboostBCEWithLogitsLossPrim()


class _PyboostBroadcastToPrim(BroadcastToPrim_):
    def __call__(self, input, shape):

        return _convert_stub(super().__call__(input, shape))


broadcast_to_impl = _PyboostBroadcastToPrim()


class _PyboostConcatPrim(ConcatPrim_):
    def __call__(self, tensors, axis):

        return _convert_stub(super().__call__(tensors, axis))


concat_impl = _PyboostConcatPrim()


class _PyboostConvolutionGradPrim(ConvolutionGradPrim_):
    def __call__(self, dout, input, weight, bias, stride, padding, dilation, transposed, output_padding, groups, output_mask):
        converted_stride = to_strides('convolution_grad', 'stride', stride)
        converted_padding = to_2d_paddings('convolution_grad', 'padding', padding)
        converted_dilation = to_dilations('convolution_grad', 'dilation', dilation)
        converted_output_padding = to_output_padding('convolution_grad', 'output_padding', output_padding)
        return _convert_stub(super().__call__(dout, input, weight, bias, converted_stride, converted_padding, converted_dilation, transposed, converted_output_padding, groups, output_mask))


convolution_grad_impl = _PyboostConvolutionGradPrim()


class _PyboostConvolutionPrim(ConvolutionPrim_):
    def __call__(self, input, weight, bias, stride, padding, dilation, transposed, output_padding, groups):
        converted_stride = to_strides('convolution', 'stride', stride)
        converted_padding = to_2d_paddings('convolution', 'padding', padding)
        converted_dilation = to_dilations('convolution', 'dilation', dilation)
        converted_output_padding = to_output_padding('convolution', 'output_padding', output_padding)
        return _convert_stub(super().__call__(input, weight, bias, converted_stride, converted_padding, converted_dilation, transposed, converted_output_padding, groups))


convolution_impl = _PyboostConvolutionPrim()


class _PyboostCrossPrim(CrossPrim_):
    def __call__(self, input, other, dim):

        return _convert_stub(super().__call__(input, other, dim))


cross_impl = _PyboostCrossPrim()


class _PyboostCummaxPrim(CummaxPrim_):
    def __call__(self, input, axis):

        return _convert_stub(super().__call__(input, axis))


cummax_impl = _PyboostCummaxPrim()


class _PyboostEluExtPrim(EluExtPrim_):
    def __call__(self, input, alpha):

        return _convert_stub(super().__call__(input, alpha))


elu_ext_impl = _PyboostEluExtPrim()


class _PyboostFFNExtPrim(FFNExtPrim_):
    def __call__(self, x, weight1, weight2, expertTokens, bias1, bias2, scale, offset, deqScale1, deqScale2, antiquant_scale1, antiquant_scale2, antiquant_offset1, antiquant_offset2, activation, inner_precise):
        converted_activation = str_to_enum('ffn_ext', 'activation', activation)
        return _convert_stub(super().__call__(x, weight1, weight2, expertTokens, bias1, bias2, scale, offset, deqScale1, deqScale2, antiquant_scale1, antiquant_scale2, antiquant_offset1, antiquant_offset2, converted_activation, inner_precise))


ffn_ext_impl = _PyboostFFNExtPrim()


class _PyboostFlashAttentionScoreGradPrim(FlashAttentionScoreGradPrim_):
    def __call__(self, query, key, value, dy, pse_shift, drop_mask, padding_mask, atten_mask, softmax_max, softmax_sum, softmax_in, attention_in, prefix, actual_seq_qlen, actual_seq_kvlen, head_num, keep_prob, scale_value, pre_tokens, next_tokens, inner_precise, input_layout, sparse_mode):
        converted_input_layout = str_to_enum('flash_attention_score_grad', 'input_layout', input_layout)
        return _convert_stub(super().__call__(query, key, value, dy, pse_shift, drop_mask, padding_mask, atten_mask, softmax_max, softmax_sum, softmax_in, attention_in, prefix, actual_seq_qlen, actual_seq_kvlen, head_num, keep_prob, scale_value, pre_tokens, next_tokens, inner_precise, converted_input_layout, sparse_mode))


flash_attention_score_grad_impl = _PyboostFlashAttentionScoreGradPrim()


class _PyboostFlashAttentionScorePrim(FlashAttentionScorePrim_):
    def __call__(self, query, key, value, real_shift, drop_mask, padding_mask, attn_mask, prefix, actual_seq_qlen, actual_seq_kvlen, head_num, keep_prob, scale_value, pre_tokens, next_tokens, inner_precise, input_layout, sparse_mode):
        converted_input_layout = str_to_enum('flash_attention_score', 'input_layout', input_layout)
        return _convert_stub(super().__call__(query, key, value, real_shift, drop_mask, padding_mask, attn_mask, prefix, actual_seq_qlen, actual_seq_kvlen, head_num, keep_prob, scale_value, pre_tokens, next_tokens, inner_precise, converted_input_layout, sparse_mode))


flash_attention_score_impl = _PyboostFlashAttentionScorePrim()


class _PyboostGridSampler2DGradPrim(GridSampler2DGradPrim_):
    def __call__(self, grad, input_x, grid, interpolation_mode, padding_mode, align_corners):
        converted_interpolation_mode = str_to_enum('grid_sampler_2d_grad', 'interpolation_mode', interpolation_mode)
        converted_padding_mode = str_to_enum('grid_sampler_2d_grad', 'padding_mode', padding_mode)
        return _convert_stub(super().__call__(grad, input_x, grid, converted_interpolation_mode, converted_padding_mode, align_corners))


grid_sampler_2d_grad_impl = _PyboostGridSampler2DGradPrim()


class _PyboostGridSampler2DPrim(GridSampler2DPrim_):
    def __call__(self, input_x, grid, interpolation_mode, padding_mode, align_corners):
        converted_interpolation_mode = str_to_enum('grid_sampler_2d', 'interpolation_mode', interpolation_mode)
        converted_padding_mode = str_to_enum('grid_sampler_2d', 'padding_mode', padding_mode)
        return _convert_stub(super().__call__(input_x, grid, converted_interpolation_mode, converted_padding_mode, align_corners))


grid_sampler_2d_impl = _PyboostGridSampler2DPrim()


class _PyboostGridSampler3DGradPrim(GridSampler3DGradPrim_):
    def __call__(self, grad, input_x, grid, interpolation_mode, padding_mode, align_corners):
        converted_interpolation_mode = str_to_enum('grid_sampler_3d_grad', 'interpolation_mode', interpolation_mode)
        converted_padding_mode = str_to_enum('grid_sampler_3d_grad', 'padding_mode', padding_mode)
        return _convert_stub(super().__call__(grad, input_x, grid, converted_interpolation_mode, converted_padding_mode, align_corners))


grid_sampler_3d_grad_impl = _PyboostGridSampler3DGradPrim()


class _PyboostGridSampler3DPrim(GridSampler3DPrim_):
    def __call__(self, input_x, grid, interpolation_mode, padding_mode, align_corners):
        converted_interpolation_mode = str_to_enum('grid_sampler_3d', 'interpolation_mode', interpolation_mode)
        converted_padding_mode = str_to_enum('grid_sampler_3d', 'padding_mode', padding_mode)
        return _convert_stub(super().__call__(input_x, grid, converted_interpolation_mode, converted_padding_mode, align_corners))


grid_sampler_3d_impl = _PyboostGridSampler3DPrim()


class _PyboostHShrinkGradPrim(HShrinkGradPrim_):
    def __call__(self, gradients, features, lambd):

        return _convert_stub(super().__call__(gradients, features, lambd))


hshrink_grad_impl = _PyboostHShrinkGradPrim()


class _PyboostHShrinkPrim(HShrinkPrim_):
    def __call__(self, input, lambd):

        return _convert_stub(super().__call__(input, lambd))


hshrink_impl = _PyboostHShrinkPrim()


class _PyboostIncreFlashAttentionPrim(IncreFlashAttentionPrim_):
    def __call__(self, query, key, value, attn_mask, actual_seq_lengths, pse_shift, dequant_scale1, quant_scale1, dequant_scale2, quant_scale2, quant_offset2, antiquant_scale, antiquant_offset, block_table, kv_padding_size, num_heads, input_layout, scale_value, num_key_value_heads, block_size, inner_precise):
        converted_input_layout = str_to_enum('incre_flash_attention', 'input_layout', input_layout)
        return _convert_stub(super().__call__(query, key, value, attn_mask, actual_seq_lengths, pse_shift, dequant_scale1, quant_scale1, dequant_scale2, quant_scale2, quant_offset2, antiquant_scale, antiquant_offset, block_table, kv_padding_size, num_heads, converted_input_layout, scale_value, num_key_value_heads, block_size, inner_precise))


incre_flash_attention_impl = _PyboostIncreFlashAttentionPrim()


class _PyboostIsClosePrim(IsClosePrim_):
    def __call__(self, input, other, rtol, atol, equal_nan):

        return _convert_stub(super().__call__(input, other, rtol, atol, equal_nan))


isclose_impl = _PyboostIsClosePrim()


class _PyboostLogSoftmaxGradPrim(LogSoftmaxGradPrim_):
    def __call__(self, logits, grad, axis):

        return _convert_stub(super().__call__(logits, grad, axis))


log_softmax_grad_impl = _PyboostLogSoftmaxGradPrim()


class _PyboostLogSoftmaxPrim(LogSoftmaxPrim_):
    def __call__(self, logits, axis):

        return _convert_stub(super().__call__(logits, axis))


log_softmax_impl = _PyboostLogSoftmaxPrim()


class _PyboostMatMulPrim(MatMulPrim_):
    def __call__(self, input, mat2, transpose_a, transpose_b):

        return _convert_stub(super().__call__(input, mat2, transpose_a, transpose_b))


matmul_impl = _PyboostMatMulPrim()


class _PyboostMaxPoolGradWithIndicesPrim(MaxPoolGradWithIndicesPrim_):
    def __call__(self, x, grad, argmax, kernel_size, strides, pads, dilation, ceil_mode, argmax_type):
        converted_kernel_size = to_kernel_size('max_pool_grad_with_indices', 'kernel_size', kernel_size)
        converted_strides = to_strides('max_pool_grad_with_indices', 'strides', strides)
        converted_pads = to_output_padding('max_pool_grad_with_indices', 'pads', pads)
        converted_dilation = to_dilations('max_pool_grad_with_indices', 'dilation', dilation)
        return _convert_stub(super().__call__(x, grad, argmax, converted_kernel_size, converted_strides, converted_pads, converted_dilation, ceil_mode, argmax_type))


max_pool_grad_with_indices_impl = _PyboostMaxPoolGradWithIndicesPrim()


class _PyboostMaxPoolGradWithMaskPrim(MaxPoolGradWithMaskPrim_):
    def __call__(self, x, grad, mask, kernel_size, strides, pads, dilation, ceil_mode, argmax_type):
        converted_kernel_size = to_kernel_size('max_pool_grad_with_mask', 'kernel_size', kernel_size)
        converted_strides = to_strides('max_pool_grad_with_mask', 'strides', strides)
        converted_pads = to_output_padding('max_pool_grad_with_mask', 'pads', pads)
        converted_dilation = to_dilations('max_pool_grad_with_mask', 'dilation', dilation)
        return _convert_stub(super().__call__(x, grad, mask, converted_kernel_size, converted_strides, converted_pads, converted_dilation, ceil_mode, argmax_type))


max_pool_grad_with_mask_impl = _PyboostMaxPoolGradWithMaskPrim()


class _PyboostMaxPoolWithIndicesPrim(MaxPoolWithIndicesPrim_):
    def __call__(self, x, kernel_size, strides, pads, dilation, ceil_mode, argmax_type):
        converted_kernel_size = to_kernel_size('max_pool_with_indices', 'kernel_size', kernel_size)
        converted_strides = to_strides('max_pool_with_indices', 'strides', strides)
        converted_pads = to_output_padding('max_pool_with_indices', 'pads', pads)
        converted_dilation = to_dilations('max_pool_with_indices', 'dilation', dilation)
        return _convert_stub(super().__call__(x, converted_kernel_size, converted_strides, converted_pads, converted_dilation, ceil_mode, argmax_type))


max_pool_with_indices_impl = _PyboostMaxPoolWithIndicesPrim()


class _PyboostMaxPoolWithMaskPrim(MaxPoolWithMaskPrim_):
    def __call__(self, x, kernel_size, strides, pads, dilation, ceil_mode, argmax_type):
        converted_kernel_size = to_kernel_size('max_pool_with_mask', 'kernel_size', kernel_size)
        converted_strides = to_strides('max_pool_with_mask', 'strides', strides)
        converted_pads = to_output_padding('max_pool_with_mask', 'pads', pads)
        converted_dilation = to_dilations('max_pool_with_mask', 'dilation', dilation)
        return _convert_stub(super().__call__(x, converted_kernel_size, converted_strides, converted_pads, converted_dilation, ceil_mode, argmax_type))


max_pool_with_mask_impl = _PyboostMaxPoolWithMaskPrim()


class _PyboostNanToNumPrim(NanToNumPrim_):
    def __call__(self, input, nan, posinf, neginf):

        return _convert_stub(super().__call__(input, nan, posinf, neginf))


nan_to_num_impl = _PyboostNanToNumPrim()


class _PyboostOneHotExtPrim(OneHotExtPrim_):
    def __call__(self, tensor, num_classes, on_value, off_value, axis):

        return _convert_stub(super().__call__(tensor, num_classes, on_value, off_value, axis))


one_hot_ext_impl = _PyboostOneHotExtPrim()


class _PyboostReduceAllPrim(ReduceAllPrim_):
    def __call__(self, input, axis, keep_dims):

        return _convert_stub(super().__call__(input, axis, keep_dims))


reduce_all_impl = _PyboostReduceAllPrim()


class _PyboostReduceAnyPrim(ReduceAnyPrim_):
    def __call__(self, x, axis, keep_dims):

        return _convert_stub(super().__call__(x, axis, keep_dims))


reduce_any_impl = _PyboostReduceAnyPrim()


class _PyboostReverseV2Prim(ReverseV2Prim_):
    def __call__(self, input, axis):

        return _convert_stub(super().__call__(input, axis))


reverse_v2_impl = _PyboostReverseV2Prim()


class _PyboostRmsNormPrim(RmsNormPrim_):
    def __call__(self, x, gamma, epsilon):

        return _convert_stub(super().__call__(x, gamma, epsilon))


rms_norm_impl = _PyboostRmsNormPrim()


class _PyboostRollPrim(RollPrim_):
    def __call__(self, input, shift, axis):

        return _convert_stub(super().__call__(input, shift, axis))


roll_impl = _PyboostRollPrim()


class _PyboostSearchSortedPrim(SearchSortedPrim_):
    def __call__(self, sorted_sequence, values, sorter, dtype, right):

        return _convert_stub(super().__call__(sorted_sequence, values, sorter, dtype, right))


searchsorted_impl = _PyboostSearchSortedPrim()


class _PyboostSoftmaxPrim(SoftmaxPrim_):
    def __call__(self, input, axis):

        return _convert_stub(super().__call__(input, axis))


softmax_impl = _PyboostSoftmaxPrim()


class _PyboostSoftShrinkGradPrim(SoftShrinkGradPrim_):
    def __call__(self, input_grad, input_x, lambd):

        return _convert_stub(super().__call__(input_grad, input_x, lambd))


softshrink_grad_impl = _PyboostSoftShrinkGradPrim()


class _PyboostSoftShrinkPrim(SoftShrinkPrim_):
    def __call__(self, input, lambd):

        return _convert_stub(super().__call__(input, lambd))


softshrink_impl = _PyboostSoftShrinkPrim()


class _PyboostStackExtPrim(StackExtPrim_):
    def __call__(self, tensors, dim):

        return _convert_stub(super().__call__(tensors, dim))


stack_ext_impl = _PyboostStackExtPrim()


class _PyboostTrilExtPrim(TrilExtPrim_):
    def __call__(self, input, diagonal):

        return _convert_stub(super().__call__(input, diagonal))


tril_ext_impl = _PyboostTrilExtPrim()


class _PyboostTriuPrim(TriuPrim_):
    def __call__(self, input, diagonal):

        return _convert_stub(super().__call__(input, diagonal))


triu_impl = _PyboostTriuPrim()


class _PyboostUpsampleTrilinear3DGradPrim(UpsampleTrilinear3DGradPrim_):
    def __call__(self, dy, input_size, output_size, scales, align_corners):

        return _convert_stub(super().__call__(dy, input_size, output_size, scales, align_corners))


upsample_trilinear3d_grad_impl = _PyboostUpsampleTrilinear3DGradPrim()


class _PyboostUpsampleTrilinear3DPrim(UpsampleTrilinear3DPrim_):
    def __call__(self, x, output_size, scales, align_corners):

        return _convert_stub(super().__call__(x, output_size, scales, align_corners))


upsample_trilinear3d_impl = _PyboostUpsampleTrilinear3DPrim()


class _PyboostGroupedMatmulPrim(GroupedMatmulPrim_):
    def __call__(self, x, weight, bias, scale, offset, antiquant_scale, antiquant_offset, group_list, split_item, group_type):

        return _convert_stub(super().__call__(x, weight, bias, scale, offset, antiquant_scale, antiquant_offset, group_list, split_item, group_type))


grouped_matmul_impl = _PyboostGroupedMatmulPrim()


class _PyboostQuantBatchMatmulPrim(QuantBatchMatmulPrim_):
    def __call__(self, x1, x2, scale, offset, bias, pertokenScaleOptional, transpose_x1, transpose_x2, dtype):

        return _convert_stub(super().__call__(x1, x2, scale, offset, bias, pertokenScaleOptional, transpose_x1, transpose_x2, dtype))


quant_batch_matmul_impl = _PyboostQuantBatchMatmulPrim()


class _PyboostWeightQuantBatchMatmulPrim(WeightQuantBatchMatmulPrim_):
    def __call__(self, x, weight, antiquant_scale, antiquant_offset, quant_scale, quant_offset, bias, transpose_x, transpose_weight, antiquant_group_size):

        return _convert_stub(super().__call__(x, weight, antiquant_scale, antiquant_offset, quant_scale, quant_offset, bias, transpose_x, transpose_weight, antiquant_group_size))


weight_quant_batch_matmul_impl = _PyboostWeightQuantBatchMatmulPrim()
