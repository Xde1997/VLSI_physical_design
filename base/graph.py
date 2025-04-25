from typing import List, Set, Dict, Any
from abc import ABC, abstractmethod
from .vertex import VertexManager, Vertex
from .edge import EdgeManager, Edge
from .partition import Partition
# from .cutset import CutSet


class Graph(ABC):
    """图的抽象基类"""

    def __init__(self):
        self.vertex_manager = VertexManager()
        self.edge_manager = EdgeManager()
        self.partition = Partition()

    def add_vertex(self, vertex_key: Any, weight: float = 1) -> Vertex:
        return self.vertex_manager.create_vertex(vertex_key, weight)

    @abstractmethod
    def add_edge(self, *args, **kwargs):
        pass

    def get_vertex(self, vertex_id: Any) -> Vertex:
        return self.vertex_manager.get_vertex_by_id(vertex_id)

    def get_vertices(self) -> List[Vertex]:
        return self.vertex_manager.get_verties()

    def get_edges(self) -> List[Edge]:
        return self.edge_manager.get_edges()

    def get_edge(self, vertexa_id: int, vertexb_id: int) -> Edge:
        return self.edge_manager.get_edge_by_vertex(vertexa_id, vertexb_id)

    def get_edge_by_id(self, edge_id: int) -> Edge:
        return self.edge_manager.get_edge_by_id(edge_id)

    def has_edge(self, vertex_id_a: int, vertex_id_b: int) -> bool:
        return self.edge_manager.get_edge_by_vertex(vertex_id_a, vertex_id_b) != None

    def get_neighbors(self, vertex_id: int) -> List[Vertex]:
        edges = self.edge_manager.get_relevant_edges(vertex_id)
        neighbors = []
        for edge in edges:
            if edge.vertices[0] == vertex_id:
                neighbors.append(
                    self.vertex_manager.get_vertex_by_id(edge.vertices[1]))
            else:
                neighbors.append(
                    self.vertex_manager.get_vertex_by_id(edge.vertices[0]))
        return neighbors

    def get_relevant_edges(self, vertex_id: int) -> List[Edge]:
        return self.edge_manager.get_relevant_edges(vertex_id)

    def get_leaf_vertices(self) -> List[int]:
        vertices = self.get_vertices()
        leaf_vertices = []
        for vertex in vertices:
            if len(self.get_neighbors(vertex.id)) == 1:
                leaf_vertices.append(vertex.id)
        return leaf_vertices

    def is_leaf_vertex(self, vertex_id: int) -> bool:
        return len(self.get_neighbors(vertex_id)) == 1

    def print(self):
        # 打印图的基本信息
        print(f"节点数量: {len(self.vertex_manager.get_vertex_keys())}")
        print(f"边的数量: {len(self.edge_manager.get_edges())}")
        print("\n图的邻接表表示:")
        for vertex in self.get_vertices():
            neighbors = self.get_neighbors(vertex.id)
            print(f"{vertex.key}: ", end="")
            for neighbor in neighbors:
                print(f"{neighbor.key} ", end="")


class UndirectedGraph(Graph):
    """无向图"""

    def add_edge(self, vertex1_key: Any, vertex2_key: Any, weight: float = 1.0) -> Edge:
        v1 = self.add_vertex(vertex1_key)
        v2 = self.add_vertex(vertex2_key)
        edge = self.edge_manager.create_edge(v1.id, v2.id, weight)
        # edge = Edge([v1, v2], weight)
        # self.edges.append(edge)
        return edge


class DirectedGraph(Graph):
    """有向图"""

    def add_edge(self, from_vertex_id: Any, to_vertex_id: Any, weight: float = 1.0) -> Edge:
        v1 = self.add_vertex(from_vertex_id)
        v2 = self.add_vertex(to_vertex_id)
        edge = Edge([v1, v2], weight)  # 第一个顶点是起点，第二个是终点
        self.edges.append(edge)
        return edge