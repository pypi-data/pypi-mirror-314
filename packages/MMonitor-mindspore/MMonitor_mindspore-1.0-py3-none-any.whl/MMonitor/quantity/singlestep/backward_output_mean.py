# 用于计算梯度的均值
from .base_class import SingleStepQuantity
import mindspore.ops as ops

class BackwardOutputMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output_grad
        return ops.mean(data)  
