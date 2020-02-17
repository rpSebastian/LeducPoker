import context
import unittest
from tree import tree_builder
from base import Node
from game import card_to_string
from settings import arg, constants


class TestCardToString(unittest.TestCase):

    def test_get_children_player_nodes(self):
        node = Node()
        node.board = card_to_string.string_to_cards('')
        node.board_string = ''
        node.street = 0
        node.current_player = constants.players.P1
        node.bets = arg.IntTensor([1, 1]).to(arg.device) 
        children = tree_builder.get_children_player_nodes(node)
        print(1)
        print(children)


if __name__ == "__main__":
    unittest.main()
    