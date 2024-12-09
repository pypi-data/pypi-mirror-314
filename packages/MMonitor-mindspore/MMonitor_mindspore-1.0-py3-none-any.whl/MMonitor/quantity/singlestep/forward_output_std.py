# 用于计算激活值的std
from .base_class import SingleStepQuantity
import mindspore as ms
class ForwardOutputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output
        return data.asnumpy().std() 

