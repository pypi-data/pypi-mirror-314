import matplotlib.pyplot as _plt


def display_len(train_dataset, test_dataset):
    print('-' * 50)
    print(f'train_dataset 的长度: {len(train_dataset)}')
    print(f'test_dataset  的长度: {len(test_dataset)}')
    print('\n' * 2)


def display_input(input):
    print('-' * 50, '\nInput:')
    print(input)
    print(f'Input 的类型: {type(input)}')
    print(f'Input.shape: {input.shape}')
    print('\n' * 2)


def display_target(target):
    print('-' * 50, '\nTarget:')
    print(target)
    print(f'Target 的类型: {type(type)}')
    print('\n' * 2)


def display_img(input, target):
    input = input.squeeze()  # squeeze() 去除单通道的维度
    fig, ax = _plt.subplots(figsize=(5, 5))
    ax.imshow(input.squeeze(), cmap='gray')
    ax.set_title(f'Label: {target}')
    ax.axis('off')
