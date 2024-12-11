class stopByAcc:
    def __init__(self, rounds, delta=0.01):
        self.rounds = rounds
        self.delta = delta
        self.max_val_acc = 0
        self.cnt = 0
    def __call__(self, val_acc):
        if val_acc < self.max_val_acc - self.delta:
            self.cnt += 1
        if val_acc >= self.max_val_acc:
            self.max_val_acc = val_acc
            self.cnt = 0
        if self.cnt > self.rounds:
            return True
        return False

class stopByLoss:
    def __init__(self, rounds, delta=0.01):
        self.rounds = rounds
        self.delta = delta
        self.min_val_loss = float('inf')
        self.cnt = 0
    def __call__(self, val_loss):
        if val_loss > self.min_val_loss + self.delta:
            self.cnt += 1
        if val_loss <= self.min_val_loss:
            self.min_val_loss = val_loss
            self.cnt = 0
        if self.cnt > self.rounds:
            return True
        return False

class reloadByLoss:
    def __init__(self, max_reload_count, reload_rounds, delta=0.01):
        '''
        基于stopByLoss\n
        max_reload_count: 最大重新加载次数\n
        reload_rounds: 多少轮内loss不减，则重新加载best_model
        '''
        self.reload_rounds = reload_rounds
        self.delta = delta
        self.min_val_loss = float('inf')
        self.cnt = 0

        self.max_reload_count = max_reload_count
        self.LOAD_CNT = 0
    def __call__(self, val_loss):
        if val_loss > self.min_val_loss + self.delta:
            self.cnt += 1
        if val_loss <= self.min_val_loss:
            self.min_val_loss = val_loss
            self.cnt = 0
        if self.cnt > self.reload_rounds:
            self.LOAD_CNT += 1
            self.cnt = 0
            if self.LOAD_CNT > self.max_reload_count:
                return 'stop'
            return 'reload'
        return 'continue'

