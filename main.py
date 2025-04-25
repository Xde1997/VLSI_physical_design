from base.graph import UndirectedGraph
from partition.kernighan_lin import kl
from partition.fiduccia_mattheyses import fm
from base.hypergraph import HyperGraph


def gen_undirected_graph():
    # 创建一个复杂的无向图
    graph = UndirectedGraph()

    # 添加节点
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
    for node in nodes:
        graph.add_vertex(node)

    # 添加边，创建一个复杂的连接结构
    edges = [
        ('A', 'B', 5), ('A', 'C', 3), ('B', 'D', 4),
        ('C', 'D', 2), ('C', 'E', 6), ('D', 'F', 1),
        ('E', 'F', 7), ('E', 'G', 8), ('F', 'H', 9),
        ('G', 'H', 2), ('G', 'I', 4), ('H', 'J', 3),
        ('I', 'J', 5), ('A', 'E', 2), ('B', 'F', 6)
    ]

    for start, end, weight in edges:
        graph.add_edge(start, end, weight)

    # 打印图的基本信息
    print(f"节点数量: {len(graph.vertex_manager.get_vertex_keys())}")
    print(f"边的数量: {len(graph.edge_manager.get_edges())}")
    print("\n图的邻接表表示:")
    for vertex in graph.get_vertices():
        neighbors = graph.get_neighbors(vertex.id)
        print(f"{vertex.key}: ", end="")
        for neighbor in neighbors:
            print(f"{neighbor.key} ", end="")
        print()
    return graph


def gen_undirected_graph_for_kl():
    # 创建一个复杂的无向图
    graph = UndirectedGraph()

    # 添加节点
    nodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    for node in nodes:
        graph.add_vertex(node)

    # 添加边，创建一个复杂的连接结构
    edges = [
        ('A', 'E', 1), ('A', 'B', 1), ('A', 'F', 1),
        ('B', 'E',  1), ('B', 'F',  1), ('E', 'F',  1),
        ('C', 'F',  1), ('C', 'G', 1), ('C', 'H', 1), ('C', 'D', 1),
        ('D', 'G', 1), ('H', 'G', 1), ('H', 'D', 1),
    ]

    for start, end, weight in edges:
        graph.add_edge(start, end, weight)

    graph.print()
    return graph


def gen_hypergraph_for_fm():
    hypergraph = HyperGraph()
    v0 = hypergraph.add_vertex('A', 2)
    v1 = hypergraph.add_vertex('B', 4)
    v2 = hypergraph.add_vertex('C', 1)
    v3 = hypergraph.add_vertex('D', 4)
    v4 = hypergraph.add_vertex('E', 5)
    hyperedge0=hypergraph.add_hyperedge([v0.id, v1.id])
    hyperedge1=hypergraph.add_hyperedge([v0.id, v1.id, v2.id])
    hyperedge2=hypergraph.add_hyperedge([v0.id, v3.id])
    hyperedge3=hypergraph.add_hyperedge([v2.id, v3.id])
    hyperedge4=hypergraph.add_hyperedge([v0.id, v4.id])
    partition = hypergraph.partition
    subpartition_a = partition.create_empty_subpartition()
    subpartition_b = partition.create_empty_subpartition()
    partition.add_vertex(hypergraph,v0.id,subpartition_a.id)
    partition.add_vertex(hypergraph,v1.id,subpartition_a.id)
    partition.add_vertex(hypergraph,v2.id,subpartition_b.id)
    partition.add_vertex(hypergraph,v3.id,subpartition_b.id)
    partition.add_vertex(hypergraph,v4.id,subpartition_b.id)

    partition.add_vertex(hypergraph,hyperedge0.get_virtual_vertex_id(),subpartition_a.id)
    partition.add_vertex(hypergraph,hyperedge1.get_virtual_vertex_id(),subpartition_a.id)
    partition.add_vertex(hypergraph,hyperedge2.get_virtual_vertex_id(),subpartition_b.id)
    partition.add_vertex(hypergraph,hyperedge3.get_virtual_vertex_id(),subpartition_b.id)
    partition.add_vertex(hypergraph,hyperedge4.get_virtual_vertex_id(),subpartition_b.id)
    hypergraph.print()
    return hypergraph


def TEST_KL():
    graph = gen_undirected_graph_for_kl()
    kl(graph)


def TEST_FM():
    hypergraph = gen_hypergraph_for_fm()
    fm(hypergraph, 0.375)


if __name__ == '__main__':
    TEST_FM()
