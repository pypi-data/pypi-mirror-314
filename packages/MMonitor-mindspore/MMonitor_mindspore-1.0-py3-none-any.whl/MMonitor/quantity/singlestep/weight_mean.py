from .base_class import SingleStepQuantity

import mindspore.ops as ops

class WeightMean(SingleStepQuantity):

    def _compute(self, global_step):
        if hasattr(self._module, 'gamma'):
            data = self._module.gamma
        else:
            data = self._module.weight
        return ops.mean(data)