from .base_class import SingleStepQuantity



class ResRatio1Save(SingleStepQuantity):

    def _compute(self, global_step):
        data = self._module.res_ratio1
        return data 
