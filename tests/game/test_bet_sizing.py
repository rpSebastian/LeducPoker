import context
import unittest
import torch
from game import bet_sizing
from settings import arg, constants
from base import Node


class TestBetSizing(unittest.TestCase):
    
    def test_get_possible_bets(self):
        node = Node()
        node.current_player = constants.players.P1
        node.street = 0
        node.bets = arg.IntTensor([1, 1]).to(arg.device)
        node.num_bets = 0
        possible_bets = bet_sizing.get_possible_bets(node)
        out = arg.IntTensor([3, 1]).to(arg.device)
        torch.testing.assert_allclose(possible_bets, out)

        node = Node()
        node.current_player = constants.players.P1
        node.street = 1
        node.bets = arg.IntTensor([3, 5]).to(arg.device)
        node.num_bets = 0
        possible_bets = bet_sizing.get_possible_bets(node)
        out = arg.IntTensor([9, 5]).to(arg.device)
        torch.testing.assert_allclose(possible_bets, out)

        node = Node()
        node.current_player = constants.players.P1
        node.street = 1
        node.bets = arg.IntTensor([3, 5]).to(arg.device)
        node.num_bets = 2
        possible_bets = bet_sizing.get_possible_bets(node)
        out = torch.empty([0, 2], dtype=arg.int_dtype).to(arg.device)
        torch.testing.assert_allclose(possible_bets, out)


if __name__ == "__main__":
    unittest.main()
