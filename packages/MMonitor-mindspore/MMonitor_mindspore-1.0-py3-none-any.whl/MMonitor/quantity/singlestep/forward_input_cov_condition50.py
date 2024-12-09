import math
import mindspore.ops as ops
from mindspore import Tensor
from .base_class import SingleStepQuantity
from MMonitor.quantity.utils.calculation import *
class ForwardInputCovCondition50(SingleStepQuantity):
    def _compute(self, global_step):
        eig_values, step = getattr(self._module, 'eig_values', (None, None))
        if eig_values is None or step is None or step != global_step:
            data = self._module.input
            cov = cal_cov_matrix(data)
            eig_values = ops.eig(cov)[0]
            real = Tensor(eig_values.asnumpy().real)
            sorted_data = ops.sort(real,descending=True)
            setattr(self._module, 'eig_values', (sorted_data[0], global_step))
        eps = 1e-7
        eig_values_float = self._module.eig_values[0]
        length = len(eig_values_float)
        index = math.floor(length * 0.5)
        eps = 1e-7
        condition50 = eig_values_float[0] / (abs(eig_values_float[index]) + eps)
        return condition50