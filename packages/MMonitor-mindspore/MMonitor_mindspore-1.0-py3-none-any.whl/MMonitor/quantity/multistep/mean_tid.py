from .base_class import MultiStepQuantity
import mindspore.ops as ops
import numpy as np
from mindspore import Tensor
class MeanTID(MultiStepQuantity):

    def _compute_ones(self, global_step):
        data = self._module.input
        return ops.mean(data)
    
    def _compute(self, global_step):
        diff_data = [d - self._module.moving_mean for d in self.cache]
        diff_data = ops.stack(diff_data)  # 使用Jittor的stack
        eps = 1e-8
        running_var = self._module.moving_variance
        if isinstance(running_var, np.ndarray):
            running_var = Tensor(running_var)
        result = diff_data.norm(dim=-1) / (ops.sqrt(running_var).norm(dim=-1) + eps)
        return result.mean()
