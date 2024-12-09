# 用于计算梯度的标准差
from .base_class import SingleStepQuantity
import mindspore.ops as ops

class BackwardInputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input_grad
        return ops.std(data)  # 使用Jittor的std计算标准差

