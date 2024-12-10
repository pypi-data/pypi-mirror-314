import numpy as _np
import matplotlib.pyplot as _plt


# 加载数据
def load_inputs_and_targets():
    inputs = [
        [1],
        [2],
        [3],
    ]

    targets = [
        [2],
        [4],
        [6],
    ]

    inputs = _np.array(inputs, dtype=_np.float32)
    targets = _np.array(targets, dtype=_np.float32)
    return inputs, targets


# 显示数据集
def display_dataset():
    inputs, targets = load_inputs_and_targets()

    print('-' * 50, '\nInputs:')
    print(inputs)
    print(f'Inputs.shape: {inputs.shape}')
    print('\n' * 2)

    print('-' * 50, '\nTargets:')
    print(targets)
    print(f'Targets.shape: {targets.shape}')
    print('\n' * 2)


# 前向传播
def forward(inputs, weights):
    outputs = _np.dot(inputs, weights)
    return outputs


# 损失函数（逐个计算）
def compute_loss(outputs, targets):
    total_loss = 0.0
    for output, target in zip(outputs, targets):
        loss = (output - target) ** 2
        total_loss += loss
    mean_squared_error = total_loss / len(targets)
    return mean_squared_error


# 损失函数（向量化）
def compute_loss_vectorized(outputs, targets):
    mean_squared_error = ((outputs - targets) ** 2).mean()
    return mean_squared_error


# 绘制损失曲线
def plot_loss(x_values, y_values, x_label='Epochs', y_label='Loss'):
    fig = _plt.figure(figsize=(6, 4))
    ax = fig.add_subplot()
    ax.plot(x_values, y_values)
    ax.xaxis.set_label_text(x_label)
    ax.yaxis.set_label_text(y_label)
    ax.grid()
    return ax
