from settings import arg
import torch


class BetSizing():
    def __init__(self):
        pass

    def get_possible_bets(self, parent_node):
        current_player = parent_node.current_player
        opponent_player = 1 - current_player
        street = parent_node.street
        opponent_bet = parent_node.bets[opponent_player]

        if parent_node.num_bets >= arg.bet_limits[street]:
            out = torch.empty([0, 2], dtype=arg.int_dtype).to(arg.device)
        else:
            out = torch.zeros([1, 2], dtype=arg.int_dtype).to(arg.device)
            out[0][opponent_player] = opponent_bet
            out[0][current_player] = opponent_bet + arg.bet_sizing[street]
        return out


bet_sizing = BetSizing()
