import torch
from settings import arg, constants
from game import TerminalEquity, card_tools
from logs import logger


class TreeValue():
    def __init__(self):
        self.terminal_equity_cache = {}

    def compute_values(self, root, starting_ranges):
        self.init_dfs(root)
        root.range = starting_ranges
        root.reach_prop = torch.ones_like(root.range)
        self.compute_ranges(root)
        self.compute_cfvs(root)
        self.compute_br_cfvs(root)
        self.compute_estimate_value(root)
        exploitability = torch.mean(torch.sum(root.br_cfv * root.range, dim=1))
        match_result = torch.mean(root.cfv * root.range, dim=1)
        logger.info('exploitability = {}, match_result = {}', exploitability, match_result)

    def compute_ranges(self, node):
        if node.terminal:
            return
        PC, AC, CC = constants.players_count, len(node.children), constants.card_count
        CP, OP = node.current_player, 1 - node.current_player
        children_ranges = torch.zeros([PC, AC, CC], dtype=arg.dtype).to(arg.device)
        ranges_expand = node.range.repeat(AC, 1, 1).transpose(0, 1)
        strategy = node.strategy
        if CP == constants.players.chance:
            children_ranges[0] = ranges_expand[0] * strategy
            children_ranges[1] = ranges_expand[1] * strategy
        else:
            children_ranges[CP] = ranges_expand[CP] * strategy
            children_ranges[OP] = ranges_expand[OP]
        for i, child in enumerate(node.children):
            child.range = children_ranges[:, i, :]
            self.compute_ranges(child)

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

    def compute_estimate_value(self, node):
        if node.terminal:
            return
        CP, AC, CC = node.current_player, len(node.children), constants.card_count
        node.estimate_value = torch.zeros([AC, CC], dtype=arg.dtype).to(arg.device)
        for i, child in enumerate(node.children):
            node.estimate_value[i] = child.cfv[CP] * child.range[CP]
        for child in node.children:
            self.compute_estimate_value(child)

    def get_terminal_equity(self, node):
        if node.board not in self.terminal_equity_cache:
            self.terminal_equity_cache[node.board] = TerminalEquity()
            self.terminal_equity_cache[node.board].set_board(node.board)
        return self.terminal_equity_cache[node.board]

    def init_dfs(self, node):
        PC, CC = constants.players_count, constants.card_count
        node.cfv = torch.zeros([PC, CC], dtype=arg.dtype).to(arg.device)
        node.br_cfv = torch.zeros([PC, CC], dtype=arg.dtype).to(arg.device)
        node.range = torch.zeros([PC, CC], dtype=arg.dtype).to(arg.device)
        for child in node.children:
            self.init_dfs(child)
