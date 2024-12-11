import torch
from torch.optim.lr_scheduler import LambdaLR


class BDecayLR(LambdaLR):
    def __init__(self, optimizer, min_lr, decay_steps=20, decay_factor=0.9):
        '''
        每训练decay_steps次, lr衰减decay_factor,
        最小不低于min_lr
        :param optimizer:
        :param min_lr:
        :param warmup_steps:
        :param decay_steps:
        :param decay_factor:
        '''
        self.optimizer = optimizer
        self.min_lr = min_lr
        self.base_lr = optimizer.param_groups[0]['lr']
        self.warmup_lr = self.base_lr * 0.1
        self.decay_factor = decay_factor
        self.decay_steps = decay_steps

        # 使用LambdaLR调度器来管理学习率
        super().__init__(optimizer, lr_lambda=self.__lr_lambda)

    def __lr_lambda(self, epoch):
        decay_epoch = epoch // self.decay_steps
        decay_lr = self.base_lr * (self.decay_factor ** decay_epoch)
        if decay_lr < self.min_lr:
            decay_lr = self.min_lr
        return decay_lr / self.base_lr  # 返回学习率的比例
