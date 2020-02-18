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


if __name__ == "__main__":
    unittest.main()
