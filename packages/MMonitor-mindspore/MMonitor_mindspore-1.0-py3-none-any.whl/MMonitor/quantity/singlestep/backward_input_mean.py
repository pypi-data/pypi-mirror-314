# 用于计算梯度的均值
from .base_class import SingleStepQuantity
import mindspore.ops as ops

class BackwardInputMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input_grad
        return ops.reduce_mean(data)
