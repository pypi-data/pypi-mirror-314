from .base_class import MultiStepQuantity
import mindspore.ops as ops

class VarTID(MultiStepQuantity):

    def _compute_ones(self, global_step):
        # 获取输入数据
        data = self._module.input
        # 计算每一行的方差的平方根（标准差）
        return ops.sqrt(ops.var(data))  # 计算标准差

    def _compute(self, global_step):
        # 获取正在运行的方差
        running_sigma = ops.sqrt(self._module.moving_variance)
        
        # 计算缓存数据与running_sigma的差值
        diff_data = [d - running_sigma for d in self.cache]
        diff_data = ops.stack(diff_data)  # 将差值堆叠起来
        
        # 定义一个非常小的 epsilon 防止除以零
        eps = 1e-8
        
        # 计算 norm，返回差异的归一化结果
        result = ops.norm(diff_data) / (ops.norm(running_sigma) + eps)
        
        # 返回最终的均值
        return result.mean()

