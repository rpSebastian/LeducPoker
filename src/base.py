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
        self.children = None
        self.action = None

        self.init = 1
        if parent_node is not None:
            self.board = parent_node.board
            self.board_string = parent_node.board_string
            self.street = parent_node.street
            self.current_player = 1 - parent_node.current_player
            self.bets = parent_node.bets.clone()
            self.num_bets = parent_node.num_bets

    def vis(self):
        return "board = {}\nstreet = {}\nplayer = {}\nbets = [{}, {}]\nterm = {}".format(
            self.board_string, self.street, self.current_player, self.bets[0].item(), self.bets[1].item(), self.terminal
        )

    def __str__(self):
        return "board = {}, street = {}, player = {}, bets = [{}, {}], term = {}".format(
            self.board_string, self.street, self.current_player, self.bets[0].item(), self.bets[1].item(), self.terminal
        )

    def __setattr__(self, name, value):
        if 'init' in self.__dict__:
            if name in self.__dict__:
                self.__dict__[name] = value
            else:
                raise Exception("name error")
        else:
            self.__dict__[name] = value


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
