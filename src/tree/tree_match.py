
import os
import torch
from settings import constants, arg
from game import card_tools, TerminalEquity
from logs import logger
import numpy as np
import random
from scipy import stats


class TreeMatch():
    def __init__(self):
        self.match_nums = 1000000
        self.terminal_equity_cache = {}

    def match(self, root):
        my_pos, opp_pos = [constants.players.P1, constants.players.P2]
        results = []
        for i in range(self.match_nums):
            cards = [i for i in range(constants.card_count)]
            random.shuffle(cards)
            my_card, opp_card, public_card = cards[:3]
            result = self.run_match(root, my_pos, opp_pos, my_card, opp_card, public_card)
            results.append(result)
            if (i + 1) % 1000 == 0:
                self.save_result(results)
                results = []
            my_pos, opp_pos = opp_pos, my_pos

    def match_using_AIVAT(self, root):
        random.seed(0)
        my_pos, opp_pos = [constants.players.P1, constants.players.P2]
        aivat_results, direct_results = [], []
        for i in range(self.match_nums):
            cards = [i for i in range(constants.card_count)]
            random.shuffle(cards)
            my_card, opp_card, public_card = cards[:3]
            aivat_result, direct_result = self.run_match_using_AIVAT(root, my_pos, opp_pos, my_card, opp_card, public_card)
            aivat_results.append(aivat_result)
            direct_results.append(direct_result)
            if (i + 1) % 1000 == 0:
                self.save_aivat_result(aivat_results, direct_results)
                aivat_results, direct_results = [], []
            my_pos, opp_pos = opp_pos, my_pos

    def save_aivat_result(self, aivat_results, direct_results):
        path = "./data/result/"
        name1 = str(arg.cfr_iters) + "_vs_" + str(arg.cfr_iters) + "_aivat" + ".npy"
        name2 = str(arg.cfr_iters) + "_vs_" + str(arg.cfr_iters) + "_direct" + ".npy"
        filename1 = path + name1
        filename2 = path + name2
        if os.path.exists(filename1):
            pre_aivat_results = np.load(filename1)
        else:
            pre_aivat_results = np.array([])
        if os.path.exists(filename2):
            pre_direct_results = np.load(filename2)
        else:
            pre_direct_results = np.array([])
        aivat_total = np.append(pre_aivat_results, aivat_results)
        direct_total = np.append(pre_direct_results, direct_results)
        np.save(filename1, aivat_total)
        np.save(filename2, direct_total)

        mean, sigma = np.mean(aivat_total), np.std(aivat_total)
        conf_int = stats.norm.interval(0.95, loc=mean, scale=sigma / np.sqrt(len(aivat_total)))
        dis = conf_int[1] - mean
        logger.debug("match = {}, aivat_result = {:.6f} ± {:.6f}, std = {:.6f}", len(aivat_total), mean, dis, sigma)

        mean, sigma = np.mean(direct_total), np.std(direct_total)
        conf_int = stats.norm.interval(0.95, loc=mean, scale=sigma / np.sqrt(len(direct_total)))
        dis = conf_int[1] - mean
        logger.debug("match = {}, direct_result = {:.6f} ± {:.6f}, std = {:.6f}", len(direct_total), mean, dis, sigma)

    def save_result(self, results):
        path = "./data/result/"
        name = str(arg.cfr_iters) + "_vs_" + str(arg.cfr_iters) + ".npy"
        filename = path + name
        if os.path.exists(filename):
            pre_results = np.load(filename)
        else:
            pre_results = np.array([])
        total = np.append(pre_results, results)
        np.save(filename, total)
        mean, sigma = np.mean(total), np.std(total)
        conf_int = stats.norm.interval(0.95, loc=mean, scale=sigma / np.sqrt(len(total)))
        dis = conf_int[1] - mean
        logger.debug("match = {}, result = {:.6f} ± {:.6f}", len(total), mean, dis)

    def run_match(self, node, my_pos, opp_pos, my_card, opp_card, public_card):
        while not node.terminal:
            if node.current_player == my_pos:
                strategy = node.strategy[:, my_card]
                action = self.choose_action(strategy)
                node = node.children[action]
            elif node.current_player == opp_pos:
                strategy = node.strategy[:, opp_card]
                action = self.choose_action(strategy)
                node = node.children[action]
            else:
                for child in node.children:
                    if child.board[0].item() == public_card:
                        node = child
                        break
        result = self.compute_utility(node, my_pos, opp_pos, my_card, opp_card, public_card)
        return result

    def compute_utility(self, node, my_pos, opp_pos, my_card, opp_card, public_card):
        if node.node_type == constants.node_types.terminal_fold:
            if node.current_player == my_pos:
                result = node.pot
            else:
                result = -node.pot
        elif node.node_type == constants.node_types.terminal_call:
            strength = card_tools.get_hand_strength(node.board)
            if strength[my_card] > strength[opp_card]:
                result = node.pot
            elif strength[my_card] < strength[opp_card]:
                result = -node.pot
            else:
                result = 0
        return result

    def choose_action(self, strategy):
        prop = random.random()
        cnt = 0
        for i, s in enumerate(strategy):
            cnt += s
            if prop < cnt:
                return i
        return len(strategy) - 1

    def compute_correction_item(self, node, action):
        range_children = torch.zeros_like(node.estimate_value)
        for i, child in enumerate(node.children):
            range_children[i] = child.range[node.current_player]
        correction_item = torch.sum(node.estimate_value * range_children / torch.sum(range_children))
        correction_item -= torch.sum(node.estimate_value[action, :] * range_children[action, :] /
                                      torch.sum(range_children[action, :]))
        return correction_item

    def run_match_using_AIVAT(self, node, my_pos, opp_pos, my_card, opp_card, public_card):
        reach_prop = card_tools.get_uniform_range(node.board)
        correction_items = 0
        while not node.terminal:
            if node.current_player == my_pos:
                strategy = node.strategy[:, my_card]
                action = self.choose_action(strategy)
                reach_prop *= node.strategy[action, :]
                correction_items += self.compute_correction_item(node, action)
                node = node.children[action]
            elif node.current_player == opp_pos:
                strategy = node.strategy[:, opp_card]
                action = self.choose_action(strategy)
                node = node.children[action]
            else:
                for i, child in enumerate(node.children):
                    if child.board[0].item() == public_card:
                        reach_prop *= node.strategy[i, :]
                        correction_items += self.compute_correction_item(node, i)
                        node = child
                        break
        terminal_equity = self.get_terminal_equity(node)
        if node.node_type == constants.node_types.terminal_call:
            equity_matrix = terminal_equity.call_matrix
        elif node.node_type == constants.node_types.terminal_fold:
            equity_matrix = terminal_equity.fold_matrix

        # 减去对手的手牌概率，以消除双方手牌的冲突
        base_value = torch.sum(equity_matrix[:, opp_card] * reach_prop[:] / (torch.sum(reach_prop[:]) - reach_prop[opp_card])) * node.pot
        if node.node_type == constants.node_types.terminal_fold and node.current_player == opp_pos:
            base_value = -base_value

        result = base_value + correction_items
        result2 = self.compute_utility(node, my_pos, opp_pos, my_card, opp_card, public_card)
        return result, result2

    def get_terminal_equity(self, node):
        if node.board not in self.terminal_equity_cache:
            self.terminal_equity_cache[node.board] = TerminalEquity()
            self.terminal_equity_cache[node.board].set_board(node.board)
        return self.terminal_equity_cache[node.board]
