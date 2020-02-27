from graphviz import Digraph
from settings import constants


class TreeVisulizer():
    def __init__(self):
        self.C1 = '#d11141'  # red
        self.C2 = '#00b159'  # green
        self.C3 = '#00aedb'  # blue
        self.C4 = '#f37735'  # orange
        self.C5 = '#ffc425'  # yellow
        self.BG = '#fffef9'  #
        self.FT = '#fffef9'
        self.FTE = '#03396c'  # edge

    def draw_node(self, node, id):
        self.g.attr('node', shape='box')
        self.g.node(name=str(id), label=node.vis())

    def draw_edge(self, par, child, par_id, cur_id):
        self.g.edge(str(par_id), str(cur_id), label=child.action)

    def dfs(self, cur_node, par_id):
        if cur_node.current_player == constants.players.chance:
            # self.cnt += 1
            # if self.cnt > 1:
            return
        for i, child in enumerate(cur_node.children):
            self.total_id += 1
            self.draw_node(child, self.total_id)
            self.draw_edge(cur_node, child, par_id, self.total_id)
            self.dfs(child, self.total_id)

    def draw_tree(self, root):
        self.cnt = 0
        self.total_id = 0
        self.g = Digraph('tree', format="png")
        self.draw_node(root, 0)
        self.dfs(root, 0)
        self.g.render(filename='tree', directory="./data/images", view=False)


tree_visulizer = TreeVisulizer()
