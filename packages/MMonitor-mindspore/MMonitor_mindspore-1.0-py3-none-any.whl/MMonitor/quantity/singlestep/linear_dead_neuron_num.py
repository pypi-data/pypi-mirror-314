from .base_class import SingleStepQuantity
import mindspore.ops as ops
from mindspore import Tensor
import mindspore
from mindspore import nn, ops


class LinearDeadNeuronNum(SingleStepQuantity):
    def _compute(self, global_step):
        # 获取模块的输出数据
        data = self._module.output
        # 将数据转换为二维形状 (batch_size, feature_size)
        output = data.view(-1, data.shape[-1])
        # 判断每一列是否符合 "死神经元" 的条件，输出小于等于 -2
        zero_num = ops.reduce_sum(ops.less_equal(output, -2), axis=0)
        # 计算死神经元的比例
        dead_neuron_ratio = ops.cast(ops.sum(zero_num), mindspore.float32) / output.shape[-1]
        return dead_neuron_ratio
