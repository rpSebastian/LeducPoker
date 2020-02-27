import torch
from settings import arg, constants
from game import TerminalEquity, card_tools
from logs import logger


class TreeCFR():
    def __init__(self):
        self.terminal_equity_cache = {}

    def run_cfr(self, root, starting_ranges):
        self.cfr_init_dfs(root)
        root.range = starting_ranges
        for iter in range(arg.cfr_iters):
            self.compute_ranges(root)
            self.compute_average_strategies(root)
            self.compute_cfvs(root)
            self.compute_regrets(root)
            self.compute_current_strategies(root)

            self.compute_ranges(root, turn="eval")
            self.compute_br_cfvs(root)
            self.compute_exploitabily(root)
            logger.debug("iter = {}, exploitability = {}", iter, root.exploitability)

    def compute_ranges(self, node, turn="train"):
        PC, AC, CC = constants.players_count, len(node.children), constants.card_count
        CP, OP = node.current_player, 1 - node.current_player
        children_ranges = torch.zeros([PC, AC, CC], dtype=arg.dtype).to(arg.device)
        ranges_expand = node.range.repeat(AC, 1, 1).transpose(0, 1)
        strategy = node.strategy if turn == "train" else node.average_strategy
        if CP == constants.players.chance:
            children_ranges[0] = ranges_expand[0] * strategy
            children_ranges[1] = ranges_expand[1] * strategy
        else:
            children_ranges[CP] = ranges_expand[CP] * strategy
            children_ranges[OP] = ranges_expand[OP]
        for i, child in enumerate(node.children):
            child.range = children_ranges[:, i, :]
            self.compute_ranges(child, turn)

    def compute_cfvs(self, node):
        PC, AC, CC = constants.players_count, len(node.children), constants.card_count
        CP, OP = node.current_player, 1 - node.current_player
        children_cfvs = torch.zeros([AC, PC, CC], dtype=arg.dtype).to(arg.device)
        for i, child in enumerate(node.children):
            self.compute_cfvs(child)
            children_cfvs[i] = child.cfv
        if node.terminal:
            terminal_equity = self.get_terminal_equity(node)
            if node.node_type == constants.node_types.terminal_call:
                equity_matrix = terminal_equity.call_matrix
            elif node.node_type == constants.node_types.terminal_fold:
                equity_matrix = terminal_equity.fold_matrix
            else:
                raise Exception()
            node.cfv[CP] = torch.matmul(equity_matrix, node.range[OP]) * node.pot
            node.cfv[OP] = torch.matmul(equity_matrix, node.range[CP]) * node.pot
            if node.node_type == constants.node_types.terminal_fold:
                node.cfv[OP] *= -1
        else:
            if CP == constants.players.chance:
                node.cfv = torch.sum(children_cfvs, dim=0)
            else:
                node.cfv[OP] = torch.sum(children_cfvs[:, OP, :], dim=0)
                node.cfv[CP] = torch.sum(node.strategy * children_cfvs[:, CP, :], dim=0)

    def compute_regrets(self, node):
        AC, CC = len(node.children), constants.card_count
        CP = node.current_player
        children_player_cfvs = torch.zeros([AC, CC], dtype=arg.dtype).to(arg.device)
        for i, child in enumerate(node.children):
            self.compute_regrets(child)
            children_player_cfvs[i] = child.cfv[CP]
        current_regret = children_player_cfvs - node.cfv[CP, :].repeat(AC, 1)
        node.regret += current_regret
        node.regret[node.regret < 1e-9] = 1e-9

    def compute_current_strategies(self, node):
        CP = node.current_player
        if CP != constants.players.chance:
            positive_regret = node.regret.clone()
            positive_regret[positive_regret < 1e-9] = 1e-9
            node.strategy = positive_regret / torch.sum(positive_regret, dim=0)
        for child in node.children:
            self.compute_current_strategies(child)

    def compute_average_strategies(self, node):
        AC, CP = len(node.children), node.current_player
        if CP != constants.players.chance:
            weight = node.range[CP].repeat(AC, 1).clone()
            weight[weight < 1e-9] = 1e-9
            node.strategy_weight_sum += weight
            weight /= node.strategy_weight_sum
            node.average_strategy = node.average_strategy * (1 - weight) + node.strategy * weight
        for child in node.children:
            self.compute_average_strategies(child)

    def compute_br_cfvs(self, node):
        PC, AC, CC = constants.players_count, len(node.children), constants.card_count
        CP, OP = node.current_player, 1 - node.current_player
        children_br_cfvs = torch.zeros([AC, PC, CC], dtype=arg.dtype).to(arg.device)
        for i, child in enumerate(node.children):
            self.compute_br_cfvs(child)
            children_br_cfvs[i] = child.br_cfv
        if node.terminal:
            terminal_equity = self.get_terminal_equity(node)
            if node.node_type == constants.node_types.terminal_call:
                equity_matrix = terminal_equity.call_matrix
            elif node.node_type == constants.node_types.terminal_fold:
                equity_matrix = terminal_equity.fold_matrix
            else:
                raise Exception()
            node.br_cfv[CP] = torch.matmul(equity_matrix, node.range[OP]) * node.pot
            node.br_cfv[OP] = torch.matmul(equity_matrix, node.range[CP]) * node.pot
            if node.node_type == constants.node_types.terminal_fold:
                node.br_cfv[OP] *= -1
        else:
            if CP == constants.players.chance:
                node.br_cfv = torch.sum(children_br_cfvs, dim=0)
            else:
                node.br_cfv[OP] = torch.sum(children_br_cfvs[:, OP, :], dim=0)
                node.br_cfv[CP] = torch.max(children_br_cfvs[:, CP, :], dim=0).values

    def compute_exploitabily(self, node):
        node.exploitability = torch.mean(torch.sum(node.br_cfv * node.range, dim=1))
        for child in node.children:
            self.compute_exploitabily(child)

    def cfr_init_dfs(self, node):
        PC, AC, CC = constants.players_count, len(node.children), constants.card_count
        node.cfv = torch.zeros([PC, CC], dtype=arg.dtype).to(arg.device)
        node.br_cfv = torch.zeros([PC, CC], dtype=arg.dtype).to(arg.device)
        node.range = torch.zeros([PC, CC], dtype=arg.dtype).to(arg.device)
        node.regret = torch.zeros([AC, CC], dtype=arg.dtype).to(arg.device)
        node.strategy_weight_sum = torch.zeros([AC, CC], dtype=arg.dtype).to(arg.device)
        if node.current_player == constants.players.chance:
            self.fill_chance_strategy(node)
        else:
            self.fill_player_strategy(node)
        node.average_strategy = node.strategy.clone()
        for child in node.children:
            self.cfr_init_dfs(child)

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

    def get_terminal_equity(self, node):
        if node.board not in self.terminal_equity_cache:
            self.terminal_equity_cache[node.board] = TerminalEquity()
            self.terminal_equity_cache[node.board].set_board(node.board)
        return self.terminal_equity_cache[node.board]
