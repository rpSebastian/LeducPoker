import context
import torch
from base import TreeParams, Node
from settings import arg, constants
from game import card_to_string, card_tools
from tree import tree_builder, TreeCFR, tree_visulizer, tree_strategy_sl


params = TreeParams()
params.root_node = Node()
params.root_node.board = card_to_string.string_to_cards('')
params.root_node.board_string = ''
params.root_node.street = 0
params.root_node.current_player = constants.players.P1
params.root_node.bets = arg.IntTensor([100, 100]).to(arg.device)
root = tree_builder.build_tree(params)

starting_range = torch.zeros([constants.players_count, constants.card_count], dtype=arg.dtype).to(arg.device)
starting_range[0] = card_tools.get_uniform_range(params.root_node.board)
starting_range[1] = card_tools.get_uniform_range(params.root_node.board)

tree_cfr = TreeCFR()
tree_cfr.run_cfr(root, starting_range)

tree_visulizer.draw_tree(root)

tree_strategy_sl.save_strategy(root)
