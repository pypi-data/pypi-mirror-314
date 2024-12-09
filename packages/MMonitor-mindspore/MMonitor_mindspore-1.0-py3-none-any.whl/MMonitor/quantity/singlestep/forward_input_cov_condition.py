from MMonitor.quantity.singlestep.base_class import SingleStepQuantity
from MMonitor.quantity.utils.calculation import *
import mindspore.ops as ops
from mindspore import Tensor

class ForwardInputCovCondition(SingleStepQuantity):
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
        condition = eig_values_float[0] / (ops.abs(eig_values_float[-1]) + eps)
        return condition