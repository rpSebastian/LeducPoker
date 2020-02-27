import context
import unittest
import torch
from game import TerminalEquity
from settings import arg, constants
from base import Node


class TestTerminalEquity(unittest.TestCase):

    def test_get_blocking_matrix(self):
        terminal_equity = TerminalEquity()
        board = torch.IntTensor([0]).to(arg.device)
        blocking_matrix = terminal_equity.get_blocking_matrix(board)

    def test_get_last_round_call_matrix(self):
        terminal_equity = TerminalEquity()
        board = torch.IntTensor([0]).to(arg.device)
        call_matrix = terminal_equity.get_last_round_call_matrix(board)

    def test_set_call_matrix(self):
        terminal_equity = TerminalEquity()
        board = torch.IntTensor([0]).to(arg.device)
        terminal_equity.set_call_matrix(board)
        print(terminal_equity.call_matrix)

    def test_set_fold_matrix(self):
        terminal_equity = TerminalEquity()
        board = torch.IntTensor([2]).to(arg.device)
        terminal_equity.set_fold_matrix(board)


if __name__ == "__main__":
    unittest.main()
