from .base_class import SingleStepQuantity


class ResRatio2Save(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.res_ratio2
        return data 

