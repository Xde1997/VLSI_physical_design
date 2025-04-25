from typing import List, Any
from .graph import Graph
from .vertex import Vertex
from .edge import Edge
from .hyperedge import HyperEdge
from .hyperedge import HyperEdgeManager


class HyperGraph(Graph):
    """超图：允许边连接多个顶点"""

    def __init__(self):
        super().__init__()
        self.edge_manager = HyperEdgeManager()

    def add_hyperedge(self, vertex_ids: List[int], weight: float = 1.0, *args, **kwargs) -> HyperEdge:
        virtual_vertex_id = self.vertex_manager.create_virtual_vertex().id
        return self.edge_manager.create_hyperedge(virtual_vertex_id, vertex_ids, weight, *args, **kwargs)

    def delete_hyperedge(self, hyperedge_id: int):
        self.edge_manager.delete_hyperedge(
            hyperedge_id, reserve_connectivity=False)

    def get_relevant_hyperedges(self, vertex_id: int) -> List[HyperEdge]:
        return self.edge_manager.get_relevant_hyperedges(vertex_id)

    def add_edge(self, vertex1_key: Any, vertex2_key: Any, weight: float = 1.0) -> Edge:
        v1 = self.add_vertex(vertex1_key)
        v2 = self.add_vertex(vertex2_key)
        edge = self.edge_manager.create_edge(v1.id, v2.id, weight)

        return edge

    def get_hyperedge_contain_edge(self, edge_id: int) -> HyperEdge:
        for hyperedge in self.edge_manager.get_hyperedges():
            if edge_id in hyperedge.edges:
                return hyperedge
        return None

    def print(self):
        print("超图信息:")
        print(f"节点数量: {len(self.vertex_manager.get_vertex_keys())}")
        print(f"虚拟节点数量: {len(self.vertex_manager.get_virtual_vertex_keys())}")
        print(f"超边数量: {len(self.edge_manager.get_hyperedges())}")
        print("\n超边列表:")
        for hyperedge in self.edge_manager.get_hyperedges():
            vertices = [self.get_vertex(vid).key for vid in hyperedge.vertices]
            print(f"超边 {hyperedge.get_virtual_vertex_id()}: {vertices}")
        print("\n分区信息:")
        self.partition.print(self)
