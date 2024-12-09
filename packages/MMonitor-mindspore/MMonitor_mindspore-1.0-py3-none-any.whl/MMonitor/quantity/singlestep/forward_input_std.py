from .base_class import SingleStepQuantity

import mindspore.ops as ops

class ForwardInputStd(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input
        return data.asnumpy().std()  # 使用Jittor的std计算标准差
