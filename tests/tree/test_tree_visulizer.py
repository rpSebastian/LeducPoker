import context
import unittest
from tree import tree_builder, tree_visulizer
from base import Node, TreeParams
from game import card_to_string
from settings import arg, constants


class TestTreeVisulizer(unittest.TestCase):

    def test_build_tree(self):
        params = TreeParams()
        params.root_node = Node()
        params.root_node.board = card_to_string.string_to_cards('')
        params.root_node.board_string = ''
        params.root_node.street = 0
        params.root_node.current_player = constants.players.P1
        params.root_node.bets = arg.IntTensor([1, 1]).to(arg.device)
        root = tree_builder.build_tree(params)
        tree_visulizer.draw_tree(root)   


if __name__ == "__main__":
    unittest.main()
