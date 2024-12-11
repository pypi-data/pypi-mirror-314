import torch
from torch.optim.lr_scheduler import LambdaLR


class BWarmupLR(LambdaLR):
    def __init__(self, optimizer, min_lr, warmup_steps=10):
        '''
        先以lr的0.1倍训练warmup_steps,
        然后回到默认的lr
        :param optimizer:
        :param min_lr:
        :param warmup_steps:
        :param decay_steps:
        :param decay_factor:
        '''
        self.optimizer = optimizer
        self.min_lr = min_lr
        self.warmup_steps = warmup_steps
        self.base_lr = optimizer.param_groups[0]['lr']
        self.warmup_lr = self.base_lr * 0.1

        # 使用LambdaLR调度器来管理学习率
        super().__init__(optimizer, lr_lambda=self.__lr_lambda)

    def __lr_lambda(self, epoch):
        if epoch < self.warmup_steps:
            # 从self.warmup_lr过度到self.base_lr
            lr = self.warmup_lr + (self.base_lr - self.warmup_lr) * (epoch / self.warmup_steps)
            return lr / self.base_lr  # 返回学习率的比例
        else:
            return 1.0  # 在warmup_steps之后，学习率保持不变
