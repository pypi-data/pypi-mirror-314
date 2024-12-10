import numpy as _np

from . import case1_v1 as _case1
from . import case2_2_v1 as _case2_2


# 加载数据
def load_inputs_and_targets(weights_true, biases_true, inputs_rows=10, increment=2, display=True):
    '''
    根据输入行数、权重矩阵和偏置向量，生成输入矩阵和目标输出。

    Args:
        weights_true (list): 权重矩阵，形状为 (输入特征数, 输出特征数)
        biases_true (list):  偏置向量，形状为 (输出特征数, )
        inputs_rows (int):   输入矩阵的行数（样本数），即生成的数据样本数量。默认值为 10
        increment (int):     每个特征列值基于此增量变化。默认值为 2。
        display (bool):      是否打印生成的输入矩阵和目标输出。默认值为 True。

    Returns:
        inputs (ndarray):   输入矩阵，形状为 (inputs_rows, 输入特征数)
        targets (ndarray): 目标输出矩阵，形状为 (inputs_rows, 输出特征数)
    '''

    weights_true = _np.array(weights_true, dtype=_np.float32)
    biases_true = _np.array(biases_true, dtype=_np.float32)

    inputs_cols = weights_true.shape[0]
    inputs = [[i + j * increment for j in range(inputs_cols)] for i in range(1, inputs_rows + 1)]
    inputs = _np.array(inputs, dtype=_np.float32)
    targets = _np.dot(inputs, weights_true) + biases_true

    if display:
        print('-' * 50, '\nWeights (W):')
        print(weights_true)
        print(f'Weights.shape: {weights_true.shape}')
        print('\n' * 2)

        print('-' * 50, '\nBiases (B):')
        print(biases_true)
        print(f'Biases.shape: {biases_true.shape}')
        print('\n' * 2)

        print('-' * 50, '\nInputs:')
        print(inputs)
        print(f'Inputs.shape: {inputs.shape}')
        print('\n' * 2)

        print('-' * 50, '\nTargets:')
        print(targets)
        print(f'Targets.shape: {targets.shape}')
        print('\n' * 2)
    return inputs, targets


# 初始化参数
init_parameters = _case2_2.init_parameters

# 前向传播
forward = _case2_2.forward

# 损失函数
compute_loss = _case2_2.compute_loss

# 梯度计算
compute_gradients = _case2_2.compute_gradients

# 格式化打印
format_and_print = _case2_2.format_and_print

# 绘制损失曲线
plot_loss = _case1.plot_loss
