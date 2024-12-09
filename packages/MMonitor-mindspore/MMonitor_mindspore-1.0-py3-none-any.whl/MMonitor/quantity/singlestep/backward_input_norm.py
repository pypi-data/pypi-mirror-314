from .base_class import SingleStepQuantity
import mindspore.ops as ops
 
class BackwardInputNorm(SingleStepQuantity):
  
   def _compute(self, global_step):
       # 获取输入梯度
       data = self._module.input_grad
       # 计算 L2 范数
       return ops.norm(data)
 