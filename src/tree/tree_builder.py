from settings import constants
from game import bet_sizing, card_tools, card_to_string
from base import Node
from logs import logger


class PokerTreeBuilder():
    def __init__(self):
        pass

    def build_tree(self, params):
        root = Node()
        root.street = params.root_node.street
        root.bets = params.root_node.bets.clone()
        root.current_player = params.root_node.current_player
        root.board = params.root_node.board.clone()
        self.num = 0
        self.build_tree_dfs(root)
        return root

    def build_tree_dfs(self, current_node):
        self.num += 1
        # logger.debug(current_node)
        children = self.get_children_nodes(current_node)
        current_node.children = children
        for child in children:
            self.build_tree_dfs(child)

    def get_children_nodes(self, parent_node):
        if parent_node.terminal:
            return []
        chance_node = parent_node.current_player == constants.players.chance
        if chance_node:
            return self.get_children_chance_nodes(parent_node)
        else:
            return self.get_children_player_nodes(parent_node)

    def get_children_chance_nodes(self, parent_node):
        children = []
        next_boards = card_tools.get_second_round_boards()
        for board in next_boards:
            chance_node = Node(parent_node)
            chance_node.current_player = constants.players.P1
            chance_node.street = parent_node.street + 1
            chance_node.board = board
            chance_node.board_string = card_to_string.cards_to_string(board)
            chance_node.num_bets = 0
            chance_node.action = chance_node.board_string
            children.append(chance_node)
        return children

    def get_children_player_nodes(self, parent_node):
        children = []

        # fold action
        fold_node = Node(parent_node)
        fold_node.terminal = True
        fold_node.action = "fold"
        children.append(fold_node)

        # P1 start check action
        if (parent_node.current_player == constants.players.P1 and
           parent_node.bets[0] == parent_node.bets[1]):
            check_node = Node(parent_node)
            check_node.action = "check"
            children.append(check_node)
        # raise -> ( P1 / P2 call ) -> chance
        # P1 check -> (P2 check ) -> chance
        elif parent_node.street == 0 and (
            parent_node.bets[0] != parent_node.bets[1] or
            parent_node.bets[0] == parent_node.bets[1] and
            parent_node.current_player == constants.players.P2
        ):
            chance_node = Node(parent_node)
            chance_node.current_player = constants.players.chance
            chance_node.bets[:] = chance_node.bets.max()
            chance_node.action = "call" if parent_node.bets[0] != parent_node.bets[1] else "check"
            children.append(chance_node)
        # call -> terminal
        else:
            terminal_call_node = Node(parent_node)
            terminal_call_node.current_player = 1 - constants.players.P2
            terminal_call_node.terminal = True
            terminal_call_node.bets[:] = terminal_call_node.bets.max()
            terminal_call_node.action = "call"
            children.append(terminal_call_node)
        # raise action
        possible_bets = bet_sizing.get_possible_bets(parent_node)
        for possible_bet in possible_bets:
            raise_node = Node(parent_node)
            raise_node.bets = possible_bet
            raise_node.num_bets += 1
            raise_node.action = "raise"
            children.append(raise_node)

        return children


tree_builder = PokerTreeBuilder()
