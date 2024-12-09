from collections import defaultdict
import numpy as np
import mindspore as ms
from mindspore import Tensor
from mindspore.ops import operations as P
from ..utils.schedules import linear 
class Quantity:

    def __init__(self, module, track_schedule=linear()):
        self._track_schedule = track_schedule
        self._module = module
        self._output = defaultdict(dict)

    def track(self, global_step):
        if self._should_compute(global_step):
            result = self._compute(global_step)
            if result is not None:
                self._save(global_step, result)

    def get_output(self):
        return self._output

    def clean_mem(self):
        self.get_output().clear()

    def _should_compute(self, global_step):
        """Return if computations need to be performed at a specific iteration."""
        raise NotImplementedError

    def _save(self, global_step, result):
        """Store computation result."""
        # 判断当前item是一个数值
        if isinstance(result,(int,float)):
            self._output[global_step] = self._apply_save_format(result)
        else:
            self._output[global_step] = self._apply_save_format(result.item())

    def _apply_save_format(self, value):
        """Apply formatting rules for saved data."""
        if isinstance(value, Tensor):
            value = value.numpy()  # 转换为numpy

        elif isinstance(value, dict):
            for key, val in value.items():
                value[key] = self._apply_save_format(val)

        elif isinstance(value, list):
            for idx, val in enumerate(value):
                value[idx] = self._apply_save_format(val)

        elif isinstance(value, tuple):
            value = tuple(self._apply_save_format(val) for val in value)

        elif isinstance(value, (float, int, np.ndarray)):
            pass

        else:
            raise NotImplementedError(f"No formatting rule for type {type(value)}")

        return value

    def _compute(self, global_step):
        """Evaluate quantity at a step in training."""
        raise NotImplementedError

    def should_show(self, global_step):
        return self._track_schedule(global_step)




