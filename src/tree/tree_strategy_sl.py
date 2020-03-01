import torch
from settings import arg


class TreeStrategySL():
    def __init__(self):
        pass

    def save_strategy(self, root):
        node_count, max_action_number = self.computer_node_info(root)
        CC = root.average_strategy.size(1)
        strategies = torch.zeros([node_count, max_action_number, CC], dtype=arg.dtype).to(arg.device)
        self.node_id = 0
        self.save_strategy_dfs(root, strategies)
        name = str(root.street) + "_" + root.board_string + "_" + str(arg.cfr_iters) + ".tch"
        path = "./data/strategy/"
        torch.save(strategies, path + name)

    def save_strategy_dfs(self, node, strategies):
        if node.terminal:
            return
        strategies[self.node_id, :len(node.children), :] = node.average_strategy.clone()
        self.node_id += 1
        for child in node.children:
            self.save_strategy_dfs(child, strategies)

    def computer_node_info(self, node):
        if node.terminal:
            return 0, 0
        node_count, max_action_number = 1, len(node.children)
        for child in node.children:
            child_node_count, child_action_number = self.computer_node_info(child)
            node_count += child_node_count
            max_action_number = max(max_action_number, child_action_number)
        return node_count, max_action_number

    def load_strategy(self, root):
        name = str(root.street) + "_" + root.board_string + "_" + str(arg.cfr_iters) + ".tch"
        path = "./data/strategy/"
        strategies = torch.load(path + name)
        self.node_id = 0
        self.load_strategy_dfs(root, strategies)

    def load_strategy_dfs(self, node, strategies):
        if node.terminal:
            return
        node.strategy = strategies[self.node_id, :len(node.children), :].clone()
        self.node_id += 1
        for child in node.children:
            self.load_strategy_dfs(child, strategies)


tree_strategy_sl = TreeStrategySL()
