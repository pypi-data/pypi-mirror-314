import mindspore.ops as ops

def cal_cov_matrix(x):
    # 如果输入为二维张量
    if x.ndim == 2:
        mean_x = ops.ReduceMean(keep_dims=True)(x, axis=0)  # 计算特征均值
        x_centered = x - mean_x  # 数据中心化
        cov_matrix = ops.MatMul(transpose_a=True)(x_centered, x_centered) / (x.shape[0] - 1)  # 协方差矩阵
        return cov_matrix

    # 如果输入为三维张量
    elif x.ndim == 3:
        x = ops.Transpose()(x, (0, 2, 1)).reshape(x.shape[2], -1)  # 调整维度并展平
        mean_x = ops.ReduceMean(keep_dims=True)(x, axis=1)  # 计算特征均值
        centered_input = x - mean_x  # 数据中心化
        cov_matrix = ops.MatMul()(centered_input, centered_input.swapaxes(0, 1)) / (x.shape[1] - 1)
        return cov_matrix

    # 如果输入为四维张量
    elif x.ndim == 4:
        x = ops.Transpose()(x, (0, 2, 3, 1)).reshape(x.shape[3], -1)  # 调整维度并展平
        mean_x = ops.ReduceMean(keep_dims=True)(x, axis=1)  # 计算特征均值
        centered_input = x - mean_x  # 数据中心化
        cov_matrix = ops.MatMul()(centered_input, centered_input.swapaxes(0, 1)) / (x.shape[1] - 1)
        return cov_matrix

def cal_eig(input):
	eigvals, _ = ops.eig(input)
	return eigvals
