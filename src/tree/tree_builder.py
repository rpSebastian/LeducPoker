from settings import constants
from game import bet_sizing
from base import Node


class PokerTreeBuilder():
    def __init__(self):
        pass

    def build_tree(self, params):
        root = Node()
        root.street = params.root_node.street
        root.bets = params.root_node.bets.clone()
        root.current_player = params.root_node.current_player
        root.board = params.root_node.board.clone()
        self.build_tree_dfs(root)

    def build_tree_dfs(self, current_node):
        children = self.get_children_nodes(current_node)
        TODO

    def get_children_nodes(self, parent_node):
        if parent_node.terminal:
            return None
        chance_node = parent_node.current_player == constants.Players.chance
        if chance_node:
            return self.get_children_chance_nodes(parent_node)
        else:
            return self.get_children_player_nodes(parent_node)
    
    def get_children_chance_nodes(self, parent_node):
        pass

    def get_children_player_nodes(self, parent_node):
        children = []

        ### fold action
        fold_node = Node(parent_node)
        fold_node.terminal = True
        children.append(fold_node)
        
        ### P1 start check action
        if parent_node.current_player == constants.players.P1 and \
           parent_node.bets[0] == parent_node.bets[2]:
            check_node = Node(parent_node)
            children.append(check_node)
        ### raise -> ( P1 / P2 call ) -> chance
        ### P1 check -> (P2 check ) -> chance
        elif street == 1 and (
            parent_node.bets[0] != parent_node.bets[1] or 
            parend_node.bets[0] == parent_node.bets[1] and \
            parent_node.current_player == constants.players.P2
        ):
            chance_node = Node(parent_node)
            chance_node.current_player = constants.players.chance
            chance_node.bets[:] = chance_node.bets.max()
            children.append(chance_node)
        ### call -> terminal
        else:
            terminal_call_node = Node(parent_node)
            terminal_call_node.current_player = 1 - constants.player.P2
            terminal_call_node.teriminal = True
            chance_node.bets[:] = chance_node.bets.max()
            children.append(terminal_call_node)
        
        ### raise action
        possible_bets = bet_sizing.get_possible_bets(parent_node)
        for possible_bet in possible_bets:
            raise_node = Node(parent_node)
            raise_node.bets = possible_bet
            children.append(raise_node)

        return children

tree_builder = PokerTreeBuilder()