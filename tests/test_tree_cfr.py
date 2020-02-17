import context
from base import TreeParams, Node
from settings.constants import constants
from game.card_to_string import card_to_string
from tree.tree_builder import PokerTreeBuilder
from settings.arguments import arg


builder = PokerTreeBuilder()
params = TreeParams()
params.root_node = Node()
params.root_node.board = card_to_string.string_to_cards('')
params.root_node.board_string = ''
params.root_node.street = 0
params.root_node.current_player = constants.players.P1
params.root_node.bets = arg.IntTensor([1, 1]).to(arg.device)
