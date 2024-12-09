from .base_class import SingleStepQuantity

import mindspore.ops as ops

class ForwardInputMean(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input
        return data.asnumpy().mean()
