from typing import List, Dict, Any
from tools.id import id_generator
from .vertex import Vertex
from abc import ABC


@id_generator
class Edge(ABC):
    """边类"""

    def __init__(self, vertices: List[int], weight: float = 1.0, use_id=True, *args, **kwargs):
        if use_id:
            self.id = Edge.get_next_id()
        self.vertices = vertices
        self.weight = weight
        for key, value in kwargs.items():
            setattr(self, key, value)

    def get_other_vertex(self, vertex_id: int) -> int:
        return self.vertices[0] if self.vertices[-1] == vertex_id else self.vertices[-1]

    def to_string(self, graph: 'Graph'):
        return f"{graph.get_vertex(self.vertices[0]).to_string()}-{graph.get_vertex(self.vertices[1]).to_string()}"

    def get_start_vertex(self) -> int:
        return self.vertices[0]

    def get_end_vertex(self) -> int:
        return self.vertices[1]


class EdgeManager(ABC):
    def __init__(self):
        self.vertex_edge_map: Dict[str, int] = {}
        self.id_edge_map: Dict[int, Edge] = {}

    def create_edge(self, v1_id: int, v2_id: int, *args, **kwargs):
        edge = Edge([v1_id, v2_id], *args, **kwargs)
        self.notify(v1_id, v2_id, edge)
        return edge

    def notify(self, v1_id: int, v2_id: int, edge: 'Edge'):
        self.id_edge_map[edge.id] = edge
        key = self._make_key(v1_id, v2_id)
        self.vertex_edge_map[key] = edge.id

    def get_edge_by_vertex(self, v1_id: int, v2_id: int) -> 'Edge':
        id = self.vertex_edge_map.get(self._make_key(v1_id, v2_id))
        if id is None:
            return None
        return self.id_edge_map[id]

    def get_edge_by_id(self, edge_id: int) -> 'Edge':
        return self.id_edge_map[edge_id]

    def clear(self):
        self.vertex_edge_map.clear()
        self.id_edge_map.clear()

    def _make_key(self, v1_id: int, v2_id: int) -> str:
        # 保证无向图时 key 一致，v1-v2 和 v2-v1 相同
        return f"{min(v1_id, v2_id)}_{max(v1_id, v2_id)}"

    def get_edges(self) -> List[Edge]:
        return list(self.id_edge_map.values())

    def get_relevant_edges(self, vertex_id: int) -> List[Edge]:
        """获取与指定顶点相关的所有边

        Args:
            vertex_id: 顶点ID

        Returns:
            List[Edge]: 包含所有相关边的列表
        """
        relevant_edges = []
        is_in = False
        for key in self.vertex_edge_map.keys():
            v1_id, v2_id = map(int, key.split('_'))
            if vertex_id == v1_id or vertex_id == v2_id:
                is_in = True
                edge_id = self.vertex_edge_map[key]
                relevant_edges.append(self.id_edge_map[edge_id])
        return relevant_edges
