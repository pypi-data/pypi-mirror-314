import numpy as _np

from . import case1_v1 as _case1
from . import case2_2_v1 as _case2_2


# 加载数据
def load_inputs_and_targets(inputs, targets):
    inputs = _np.array(inputs, dtype=_np.float32)
    targets = _np.array(targets, dtype=_np.float32)
    return inputs, targets


# 初始化参数
def init_parameters(inputs, hidden_size, targets):
    n_features = len(inputs[0])
    n_outputs = len(targets[0])

    w1 = _np.zeros((n_features, hidden_size))  # (n_features, n_hiddens)
    b1 = _np.zeros(hidden_size)  # (n_hiddens,)
    w2 = _np.zeros((hidden_size, n_outputs))  # (n_hiddens, n_outputs)
    b2 = _np.zeros(n_outputs)  # (n_outputs,)
    return w1, b1, w2, b2


# Sigmoid 激活函数
def sigmoid(x):
    return 1 / (1 + _np.exp(-x))


# Sigmoid 激活函数的导数
def sigmoid_derivative(x):
    return sigmoid(x) * (1 - sigmoid(x))


# 前向传播
def forward(X, w1, b1, w2, b2):
    # X: (n_samples, n_features)

    z1 = _np.dot(X, w1) + b1  # (n_samples, n_hidden)
    h = sigmoid(z1)  # (n_samples, n_hidden)
    z2 = _np.dot(h, w2) + b2  # (n_samples, n_outputs)
    y_hat = z2  # 线性输出
    return z1, h, z2, y_hat


# 损失函数
compute_loss = _case2_2.compute_loss


# 反向传播
def backward(X, Y, z1, h, z2, y_hat, w2):
    # X: (n_samples, n_features)
    # Y: (n_samples, n_outputs)
    # y_hat: (n_samples, n_outputs)

    # 输出层误差
    delta_output = y_hat - Y  # (n_samples, n_outputs)

    # 隐藏层误差
    # w2: (n_hidden, n_outputs)
    # delta_output * w2.T: (n_samples, n_outputs)
    # sigmoid_derivative(z1): (n_samples, n_hidden)
    delta_hidden = (delta_output @ w2.T) * sigmoid_derivative(z1)

    # 梯度计算
    # h: (n_samples, n_hidden)
    # delta_output: (n_samples, n_outputs)
    grad_w2 = h.T @ delta_output  # (n_hidden, n_outputs)
    grad_b2 = _np.sum(delta_output, axis=0)  # (n_outputs,)

    # X: (n_samples, n_features)
    # delta_hidden: (n_samples, n_hidden)
    grad_w1 = X.T @ delta_hidden  # (n_features, n_hidden)
    grad_b1 = _np.sum(delta_hidden, axis=0)  # (n_hidden,)

    return grad_w1, grad_b1, grad_w2, grad_b2


# 格式化打印
def format_and_print(epoch, loss, inputs, w1, b1, w2, b2):
    _, _, _, y_hat = forward(inputs, w1, b1, w2, b2)
    y_hat = ' '.join(f'{x:.1f}' for x in y_hat.flatten())
    print(f'Epoch={epoch} Loss={loss:.3f} Outputs=[{y_hat}]')


# 绘制损失曲线
plot_loss = _case1.plot_loss
