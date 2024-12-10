import torch as _torch

from . import case7_v1 as _case7

_torch.manual_seed(168)

# 加载数据
load_inputs_and_targets = _case7.load_inputs_and_targets

# 显示数据集
display_dataset = _case7.display_dataset
