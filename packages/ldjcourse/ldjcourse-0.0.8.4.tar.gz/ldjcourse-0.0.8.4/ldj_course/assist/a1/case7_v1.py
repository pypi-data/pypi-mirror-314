import torch as _torch

_torch.manual_seed(168)


# 加载数据
def load_inputs_and_targets(inputs_rows=20, coefficients=None, noise_factor=1):
    inputs = _torch.arange(0, inputs_rows, dtype=_torch.float32)
    inputs = inputs.view(-1, 1)

    if coefficients is None:
        a, b, c = 0, 2, 5
    else:
        a, b, c = coefficients
    targets = a * inputs * inputs + b * inputs + c

    # noise_factor 噪声的标准差
    noise = noise_factor * _torch.randn_like(targets)  # 生成与targets同样形状的噪声
    targets += noise
    return inputs, targets


# 显示数据集
def display_dataset(inputs, targets):
    print('-' * 50, '\nInputs:')
    print(inputs)
    print(f'Inputs.shape: {inputs.shape}')
    print('\n' * 2)

    print('-' * 50, '\nTargets:')
    print(targets)
    print(f'Targets.shape: {targets.shape}')
    print('\n' * 2)
