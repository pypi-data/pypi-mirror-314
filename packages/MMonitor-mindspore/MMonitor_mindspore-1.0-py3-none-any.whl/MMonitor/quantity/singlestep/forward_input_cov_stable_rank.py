from regex import P
from .base_class import SingleStepQuantity
from mindspore import Tensor
import mindspore.ops as ops
from MMonitor.quantity.utils.calculation import *
class ForwardInputCovStableRank(SingleStepQuantity):
    def _compute(self, global_step):
        eig_values, step = getattr(self._module, 'eig_values', (None, None))
        if eig_values is None or step is None or step != global_step:
            data = self._module.input
            cov = cal_cov_matrix(data)
            eig_values = ops.eig(cov)[0]
            real = Tensor(eig_values.asnumpy().real)
            sorted_data = ops.sort(real,descending=True)
            setattr(self._module, 'eig_values', (sorted_data[0], global_step))
        eig_values_float = self._module.eig_values[0]
        max_eigen_value = eig_values_float[0]
        eig_sum = eig_values_float.sum()
        if max_eigen_value == 0:
            return eig_sum * 0
        stable_rank = eig_sum / max_eigen_value
        return stable_rank

