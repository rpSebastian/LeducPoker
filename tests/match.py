import context
import torch
from base import TreeParams, Node
from settings import arg, constants
from game import card_to_string, card_tools
from tree import tree_builder, tree_visulizer, tree_strategy_sl, TreeMatch, TreeValue


params = TreeParams()
params.root_node = Node()
params.root_node.board_string = arg.board_string
params.root_node.board = card_to_string.string_to_cards(arg.board_string)
params.root_node.street = arg.street
params.root_node.current_player = constants.players.P1
params.root_node.bets = arg.IntTensor([1, 1]).to(arg.device)
root = tree_builder.build_tree(params)

tree_strategy_sl.load_strategy(root)

starting_ranges = torch.zeros([constants.players_count, constants.card_count], dtype=arg.dtype).to(arg.device)
starting_ranges[0] = card_tools.get_uniform_range(params.root_node.board)
starting_ranges[1] = card_tools.get_uniform_range(params.root_node.board)
TreeValue().compute_values(root, starting_ranges)

tree_match = TreeMatch()
tree_match.match_using_AIVAT(root)
