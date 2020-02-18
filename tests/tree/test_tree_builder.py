import context
import unittest
from tree import tree_builder
from base import Node, TreeParams
from game import card_to_string
from settings import arg, constants
from logs import logger


class TestCardToString(unittest.TestCase):

    def test_get_children_player_nodes(self):
        node = Node()
        node.board_string = 'Jc'
        node.board = card_to_string.string_to_cards(node.board_string)
        node.street = 1
        node.num_bets = 2
        node.current_player = constants.players.P1
        node.bets = arg.IntTensor([1, 1]).to(arg.device) 
        children = tree_builder.get_children_player_nodes(node)
        for child in children:
            pass
            # print(child)

    def test_get_children_chance_nodes(self):
        node = Node()
        node.board_string = ''
        node.board = card_to_string.string_to_cards(node.board_string)
        node.street = 0
        node.num_bets = 0
        node.current_player = constants.players.P1
        node.bets = arg.IntTensor([1, 1]).to(arg.device) 
        children = tree_builder.get_children_chance_nodes(node)
        for child in children:
            pass
            # print(child)

    def test_build_tree(self):
        params = TreeParams()
        params.root_node = Node()
        params.root_node.board = card_to_string.string_to_cards('')
        params.root_node.board_string = ''
        params.root_node.street = 0
        params.root_node.current_player = constants.players.P1
        params.root_node.bets = arg.IntTensor([1, 1]).to(arg.device)
        root = tree_builder.build_tree(params)
        self.terminal_node = 0
        self.chacne_node = 0
        self.else_node = 0
        self.dfs(root)
        # logger.debug("{} {} {}", self.terminal_node, self.chacne_node, self.else_node)

    def dfs(self, root):
        if root.terminal:
            self.terminal_node += 1
        elif root.current_player == constants.players.chance:
            self.chacne_node += 1
        else:
            self.else_node += 1
        if root.current_player == constants.players.chance:
            return

        for child in root.children:
            self.dfs(child)


if __name__ == "__main__":
    unittest.main()
   