# 用于计算梯度的标准差
from .base_class import SingleStepQuantity
import mindspore.ops as ops

class BackwardOutputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output_grad
        return ops.std(data)  