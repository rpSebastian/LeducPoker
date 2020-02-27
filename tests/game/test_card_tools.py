import context
import torch
import unittest
from game import card_tools
from settings import arg


class TestCardTools(unittest.TestCase):

    def test_get_second_round_boards(self):
        boards = card_tools.get_second_round_boards()
        out = arg.IntTensor([[0], [1], [2], [3], [4], [5]]).to(arg.device)
        torch.testing.assert_allclose(boards, out)

    def test_board_to_street(self):
        board = arg.IntTensor([]).to(arg.device)
        street = card_tools.board_to_street(board)
        self.assertEqual(street, 0)

        board = arg.IntTensor([2]).to(arg.device)
        street = card_tools.board_to_street(board)
        self.assertEqual(street, 1)

    def test_get_hand_strength(self):
        board = arg.IntTensor([5]).to(arg.device)
        strength = card_tools.get_hand_strength(board)
        out = arg.IntTensor([1, 1, 2, 2, 4, 4]).to(arg.device)
        torch.testing.assert_allclose(strength, out)

    def test_get_possible_hand_index(self):
        board = arg.IntTensor([5]).to(arg.device)
        possible_hand = card_tools.get_possible_hand_index(board)
        out = arg.IntTensor([1, 1, 1, 1, 1, 0]).to(arg.device)
        torch.testing.assert_allclose(possible_hand, out)


if __name__ == "__main__":
    unittest.main()
