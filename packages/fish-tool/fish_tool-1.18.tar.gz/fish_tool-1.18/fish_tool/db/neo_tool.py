from tqdm import tqdm
from fish_tool.log_tool import logs, InfoError

try:
    import py2neo
except ImportError:
    py2neo = ImportError('未载入 py2neo')
    logs.tmp.warning(f'未载入模块 py2neo')


# a = Node('测试-人', name='张三')
# b = Node('测试-人', name='李四', 性别='男')
# # r = Relationship(a, '认识', b)
# print(a)
# print(b)


def node_str_fn(self):
    label = ','.join(self._labels)
    kv = dict(self)
    txt = f'(:{label} {kv})'
    return txt


def node_label_txt(self):
    vs = list(self._labels)
    return ','.join(vs)


if py2neo:
    py2neo.Node.__str__ = node_str_fn  # 修复Node显示中文乱码的问题
    py2neo.Node.label = node_label_txt  # 添加一个函数方便提取node的label


class NeoTool:
    def __init__(self, host='bolt://localhost:7687', user='neo4j', password='neo'):
        self.graph = py2neo.Graph(host, auth=(user, password))
        logs.brief.info(f'已连结neo4j {user}@{host}')

    def graph_run(self, query):
        resp = self.graph.run(query)
        xx = resp.to_subgraph()
        yy = resp.data()

    def get_node(self, name):
        query = f'MATCH (n) WHERE n.name = "{name}" RETURN n'
        node = self.graph.run(query).to_subgraph()
        return node

    def match_nodes(self, query='', k=None, v=None):
        # 获取 节点
        if k and v:
            query = f' WHERE n.{k} = "{v}"'
        txt = f'MATCH (n){query} RETURN n'
        g = self.graph.run(txt).to_subgraph()
        out = [node for node in g.nodes]
        return out

    def match_rels(self, nodes=None, r_type=None, limit=None):
        # 获取 关系 （图数据库优化的是图计算，也就是节点的连接关系，连通性之类的这些，查询关系比较慢）
        rels = self.graph.match(nodes=nodes, r_type=r_type, limit=limit)
        print(len(rels))
        out = []
        for rel in tqdm(rels, desc='iter relation', leave=False):
            out.append(rel)
        return out

    def delete(self, query):
        # query = 'MATCH (n) WHERE n.name = "张三" RETURN n'
        nodes = self.graph.run(query).to_subgraph()
        self.graph.delete(nodes)

    def add_node(self, label, **kv):
        node = py2neo.Node(label, **kv)
        self.graph.create(node)
        return node

    def add_relation(self, node1, label, node2):
        rel = py2neo.Relationship(node1, label, node2)
        self.graph.create(rel)
        return rel

    @staticmethod
    def query_all_node():
        return 'MATCH (n) RETURN n'

    def add_rel_by_name(self, name1, rel, name2):
        # 通过节点name添加关系
        node1 = self.get_node(name1)
        node2 = self.get_node(name2)
        if node1 is not None and node2 is not None:
            self.add_relation(node1, rel, node2)
            logs.tmp.info(f'{name1}-{rel}->{name2}')
        else:
            logs.tmp.error(f'node1={node1}  node2={node2}')
            raise InfoError('添加关系失败  节点未找到')


if __name__ == '__main__':
    # db = NeoTool()
    # node = db.get_node('name', '吸血鬼')
    # print(node)

    node = py2neo.Node('标签', 权重='中文', 维度=['中文', '中午'])
    print(node)
    # print(str(node))
    # print(node_str(node))
