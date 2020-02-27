import torch
from game import card_tools
from settings import constants, arg


class TreeStrategyFilling():
    def __init__(self):
        pass

    def fill_chance_strategy(self, node):
        action_count = len(node.children)
        node.strategy = torch.ones([action_count, constants.card_count], dtype=arg.dtype).to(arg.device)
        for i, child in enumerate(node.children):
            mask = card_tools.get_possible_hand_index(child.board)
            node.strategy[i] = node.strategy[i] * mask / (constants.card_count - 2)

    def fill_player_strategy(self, node):
        action_count = len(node.children)
        node.strategy = torch.ones([action_count, constants.card_count], dtype=arg.dtype).to(arg.device)
        node.strategy /= action_count

    def fill_uniform_strategy(self, node):
        if node.terminal:
            return
        if node.current_player == constants.players.chance:
            self.fill_chance_strategy(node)
        else:
            self.fill_player_strategy(node)
        for child in node.children:
            self.fill_uniform_strategy(child)


strategy_filling = TreeStrategyFilling()
