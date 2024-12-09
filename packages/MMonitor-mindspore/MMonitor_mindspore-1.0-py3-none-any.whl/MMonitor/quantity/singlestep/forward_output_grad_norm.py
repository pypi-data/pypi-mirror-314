# 用于计算激活值的norm
from .base_class import SingleStepQuantity
import mindspore.ops as ops

class ForwardOutputNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        data = ops.flatten(data)
        return ops.norm(data)

