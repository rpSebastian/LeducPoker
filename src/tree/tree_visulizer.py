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

    def draw_edge(self, child, par_id, cur_id):
        self.g.edge(str(par_id), str(cur_id), label=child.action)

    def dfs(self, cur_node, par_id):
        # if cur_node.current_player == constants.players.chance:
        #     return
        for child in cur_node.children:
            self.total_id += 1
            self.draw_node(child, self.total_id)
            self.draw_edge(child, par_id, self.total_id)
            self.dfs(child, self.total_id)

    def draw_tree(self, root):
        self.total_id = 0
        self.g = Digraph('tree', format="png")
        self.draw_node(root, 0)
        self.dfs(root, 0)
        self.g.render(filename='tree', directory="./data/images", view=False)


tree_visulizer = TreeVisulizer()

# # 实例化一个Digraph对象(有向图)，name:生成的图片的图片名，format:生成的图片格式
# dot = Digraph(name="MyPicture", comment="the test", format="png")

# # 生成图片节点，name：这个节点对象的名称，label:节点名,color：画节点的线的颜色
# dot.node(name='a', label='Ming', color='green')
# dot.node(name='b', label='Hong', color='yellow')
# dot.node(name='c', label='Dong')

# # 在节点之间画线，label：线上显示的文本,color:线的颜色
# dot.edge('a', 'b', label="ab\na-b", color='red')
# # 一次性画多条线，c到b的线，a到c的线
# dot.edges(['cb', 'ac'])

# # 跟view一样的用法(render跟view选择一个即可)，一般用render生成图片，不使用view=True,view=True用在调试的时候
