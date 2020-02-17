class TreeParams():
    def __init__(self):
        self.root_node = None


class Node():
    def __init__(self, parent_node=None):
        self.board = None
        self.board_string = None
        self.street = None
        self.current_player = None
        self.bets = None
        self.terminal = False
        self.num_bets = 0

        if parent_node is not None:
            self.board = parent_node.board
            self.board_string = parent_node.board_string
            self.street = parent_node.street
            self.bets = parent_node.bets.clone()
            self.current_player = 1 - parent_node.current_player


class Players():
    def __init__(self):
        self.chance = None
        self.P1 = None
        self.P2 = None


class NodeTypes():
    def __init__(self):
        self.terminal_fold = None
        self.terminal_call = None
        self.check = None
        self.chance_node = None
        self.inner_node = None
