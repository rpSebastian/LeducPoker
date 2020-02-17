from base import Players, NodeTypes


class Constants():
    def __init__(self):
        # the number of players in the game
        self.players_count = 2
        # the number of betting rounds in the game
        self.streets_count = 2

        self.suit_count = 4
        self.rank_count = 13
        self.card_count = self.suit_count * self.rank_count

        # IDs for each player and chance
        self.players = Players()
        self.players.chance = -1
        self.players.P1 = 0
        self.players.P2 = 1

        # IDs for terminal nodes (either after a fold or call action) and nodes that follow a check action
        # @field terminal_fold (terminal node following fold) `-2`
        # @field terminal_call (terminal node following call) `-1`
        # @field chance_node (node for the chance player) `0`
        # @field check (node following check) `-1`
        # @field inner_node (any other node) `2`
        self.node_types = NodeTypes()
        self.node_types.terminal_fold = -2
        self.node_types.terminal_call = -1
        self.node_types.check = -1
        self.node_types.chance_node = 0
        self.node_types.inner_node = 1


constants = Constants()
