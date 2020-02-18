import torch
from settings import constants, arg


class CardTools():
    def __init__(self):
        pass

    def get_second_round_boards(self):
        out = torch.empty([constants.card_count, constants.board_card_count], dtype=arg.int_dtype).to(arg.device)
        for i in range(constants.card_count):
            out[i, 0] = i
        return out


card_tools = CardTools()
