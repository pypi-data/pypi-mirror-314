import torch as _torch

from . import case1_v1 as _case1


# 加载数据
def load_inputs_and_targets(inputs, targets):
    inputs = _torch.tensor(inputs, dtype=_torch.float32)
    targets = _torch.tensor(targets, dtype=_torch.float32)
    return inputs, targets


# 格式化打印
def format_and_print(epoch, loss, outputs):
    y_hat = outputs.detach().numpy()
    y_hat = ' '.join(f'{x:.1f}' for x in y_hat.flatten())
    print(f'Epoch={epoch} Loss={loss:.3f} Outputs=[{y_hat}]')


# 绘制损失曲线
plot_loss = _case1.plot_loss


def print_model_parameters(model):
    '''
    打印模型的所有可训练参数的名称、值和形状。
    '''

    for param_name, param_value in model.named_parameters():
        print(f'Parameter name: {param_name}')
        print(f'Parameter value: {param_value.data}')
        print(f'Parameter shape: {param_value.shape}')
        print('-' * 50)
