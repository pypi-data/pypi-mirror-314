import torch as _torch

from . import case6_v1 as _case6

_torch.manual_seed(168)

# 加载数据
load_inputs_and_targets = _case6.load_inputs_and_targets

# 显示数据集
display_dataset = _case6.display_dataset
