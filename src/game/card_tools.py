import torch
from settings import constants, arg
from game import card_to_string


class CardTools():
    def __init__(self):
        pass

    def get_second_round_boards(self):
        out = torch.empty([constants.card_count, constants.board_card_count[1]], dtype=arg.int_dtype).to(arg.device)
        for i in range(constants.card_count):
            out[i, 0] = i
        return out

    def board_to_street(self, board):
        for street in [0, 1]:
            if board.nelement() == constants.board_card_count[street]:
                return street
        raise Exception()

    def get_hand_strength(self, board):
        rank = dict(J=1, Q=2, K=3)
        board_card = board[0].item()
        board_rank = card_to_string.card_to_rank(board_card)
        strength = torch.empty([constants.card_count], dtype=arg.dtype).to(arg.device)
        for i, card in enumerate(range(constants.card_count)):
            card_rank = card_to_string.card_to_rank(card)
            if board_rank == card_rank:
                strength[i] = 4
            else:
                strength[i] = rank[card_rank]
        return strength

    def get_possible_hand_index(self, board):
        possible_hand = torch.ones([constants.card_count], dtype=arg.int_dtype).to(arg.device)
        for board_card in board:
            possible_hand[board_card] = 0
        return possible_hand

    def get_uniform_range(self, board):
        possible_hand = self.get_possible_hand_index(board).type(arg.Tensor)
        uniform_range = possible_hand / torch.sum(possible_hand)
        return uniform_range


card_tools = CardTools()
