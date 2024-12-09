# 用于计算激活值的均值
from .base_class import SingleStepQuantity
import mindspore.ops as ops

class ForwardOutputMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        return ops.mean(data)  # 使用Jittor的norm计算L2范数

