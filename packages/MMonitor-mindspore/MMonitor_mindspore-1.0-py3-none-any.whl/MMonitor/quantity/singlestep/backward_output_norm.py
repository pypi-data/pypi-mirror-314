from .base_class import SingleStepQuantity
import mindspore.ops as ops

class BackwardOutputNorm(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.output_grad
        return ops.norm(data)  
