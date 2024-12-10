import numpy as _np

from . import case1_v1 as _case1


# 加载数据
def load_inputs_and_targets():
    inputs = [
        [1],
        [2],
        [3],
    ]

    targets = [
        [2 + 1],
        [4 + 1],
        [6 + 1],
    ]

    inputs = _np.array(inputs, dtype=_np.float32)
    targets = _np.array(targets, dtype=_np.float32)
    return inputs, targets


# 初始化参数
def init_parameters(inputs, targets):
    n_features = len(inputs[0])
    n_outputs = len(targets[0])

    weights = _np.zeros((n_features, n_outputs))
    bias = _np.zeros(n_outputs)
    return weights, bias


# 前向传播
def forward(inputs, weights, bias):
    outputs = _np.dot(inputs, weights) + bias
    return outputs


# 损失函数
def compute_loss(outputs, targets):
    mean_squared_error = ((outputs - targets) ** 2).mean()
    return mean_squared_error


# 梯度计算
def compute_gradients(inputs, outputs, targets):
    grad_weights = -2 * _np.dot(inputs.T, targets - outputs) / len(targets)
    grad_bias = -2 * (targets - outputs).mean(axis=0)
    return grad_weights, grad_bias


# 格式化打印
def format_and_print(epoch, loss, weights, bias):
    weights = ' '.join(f'{w:.3f}' for w in weights.flatten())
    bias = ' '.join(f'{b:.3f}' for b in bias)
    print(f'Epoch={epoch} Loss={loss:.3f} Weights=[{weights}] Bias=[{bias}]')


# 绘制损失曲线
plot_loss = _case1.plot_loss
