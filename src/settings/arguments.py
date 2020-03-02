import torch


class Arguments():
    def __init__(self):
        self.gpu = False
        self.dtype = torch.float32
        self.int_dtype = torch.int64
        self.Tensor = torch.FloatTensor
        self.IntTensor = torch.Tensor
        self.device = torch.device("cuda:0") if self.gpu else torch.device("cpu")
        self.bet_sizing = [2, 4]
        self.bet_limits = [2, 2]
        self.cfr_iters = 3000

        self.board_string = ""
        self.street = 0


arg = Arguments()
