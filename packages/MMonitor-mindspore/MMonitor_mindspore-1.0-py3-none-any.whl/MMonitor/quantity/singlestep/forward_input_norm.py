from MMonitor.quantity.singlestep.base_class import SingleStepQuantity
import mindspore.numpy as np
class ForwardInputNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.input
        return np.norm(data)


