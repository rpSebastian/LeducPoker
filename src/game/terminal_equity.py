import torch
from settings import arg, constants
from game import card_tools


class TerminalEquity():
    def __init__(self):
        pass

    def set_call_matrix(self, board):
        street = card_tools.board_to_street(board)
        if street == 0:
            self.call_matrix = torch.zeros([constants.card_count, constants.card_count], dtype=arg.dtype).to(arg.device)
            next_round_boards = card_tools.get_second_round_boards()
            for board in next_round_boards:
                next_round_equity_matrix = self.get_last_round_call_matrix(board)
                self.call_matrix += next_round_equity_matrix
            self.call_matrix /= (constants.card_count - 2)
        elif street == 1:
            self.call_matrix = self.get_last_round_call_matrix(board)

    def get_last_round_call_matrix(self, board):
        strength = card_tools.get_hand_strength(board)
        strength_col = strength.view(-1, 1).clone()
        strength_row = strength.view(1, -1).clone()
        matrix = (strength_col > strength_row).int() - (strength_col < strength_row).int()
        blocking_matrix = self.get_blocking_matrix(board)
        last_round_call_matrix = (matrix * blocking_matrix).float()
        return last_round_call_matrix

    def get_blocking_matrix(self, board):
        possible_hand_index = card_tools.get_possible_hand_index(board)
        hand_count = possible_hand_index.size(0)
        blocking_matrix1 = possible_hand_index.view(1, hand_count).clone().repeat(hand_count, 1)
        blocking_matrix2 = possible_hand_index.view(hand_count, 1).clone().repeat(1, hand_count)
        blocking_matrix = blocking_matrix1 * blocking_matrix2
        for i in range(blocking_matrix.size(0)):
            blocking_matrix[i, i] = 0
        return blocking_matrix

    def set_fold_matrix(self, board):
        self.fold_matrix = torch.ones([constants.card_count, constants.card_count], dtype=arg.dtype).to(arg.device)
        blocking_matrix = self.get_blocking_matrix(board)
        self.fold_matrix *= blocking_matrix

    def set_board(self, board):
        self.set_call_matrix(board)
        self.set_fold_matrix(board)
