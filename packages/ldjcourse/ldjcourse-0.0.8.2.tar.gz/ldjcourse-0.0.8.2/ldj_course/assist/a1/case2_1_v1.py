import numpy as _np

from . import case1_v1 as _case1

# 加载数据
load_inputs_and_targets = _case1.load_inputs_and_targets


# 初始化参数
def init_parameters(inputs, targets):
    n_features = len(inputs[0])
    n_outputs = len(targets[0])

    weights = _np.zeros((n_features, n_outputs))
    return weights


# 前向传播
forward = _case1.forward

# 损失函数
compute_loss = _case1.compute_loss_vectorized


# 梯度计算
def compute_gradients(inputs, outputs, targets):
    gradients = -2 * _np.dot(inputs.T, targets - outputs) / len(targets)
    return gradients


# 格式化打印
def format_and_print(epoch, loss, weights):
    weights = ' '.join(f'{w:.3f}' for w in weights.flatten())
    print(f'Epoch={epoch} Loss={loss:.3f} Weights=[{weights}]')


# 绘制损失曲线
plot_loss = _case1.plot_loss
