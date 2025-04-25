from typing import List, Dict, Set
from .edge import Edge
from tools.id import id_generator
from .vertex import Vertex
from .edge import EdgeManager


@id_generator
class HyperEdge:
    def __init__(self, virtual_vertex_id: int, vertices: List[int], weight: float, *args, **kwargs):
        self.id = HyperEdge.get_next_id()
        self.virtual_vertex_id = virtual_vertex_id
        self.vertices = vertices
        self.edges = []
        self.weight = weight
        for key, value in kwargs.items():
            setattr(self, key, value)

    def is_contain_vertex(self, vertex_id: int) -> bool:
        return vertex_id in self.vertices or self.virtual_vertex_id == vertex_id

    def get_edges(self) -> List[int]:
        return self.edges
    def get_vertices(self) -> List[int]:
        return self.vertices

    def get_virtual_vertex_id(self) -> int:
        return self.virtual_vertex_id

class HyperEdgeManager(EdgeManager):
    def __init__(self):
        super().__init__()
        self.id_hyperedge_map: Dict[int, HyperEdge] = {}  # edge_id -> Edge 实例

    def create_hyperedge(self, virtual_vertex_id: int, vertex_ids: List[int], weight: float = 1.0, *args, **kwargs) -> 'HyperEdge':
        hyperedge = HyperEdge(
            virtual_vertex_id, vertex_ids, weight, *args, **kwargs)
        self.id_hyperedge_map[hyperedge.id] = hyperedge
        for vid in vertex_ids:
            edge = self.create_edge(
                vid, virtual_vertex_id, weight, *args, **kwargs)
            hyperedge.edges.append(edge.id)
        return hyperedge

    def get_hyperedge_by_id(self, hyperedge_id: int) -> 'HyperEdge':
        return self.id_hyperedge_map.get(hyperedge_id)

    def is_hyperedge(self, vertex_id: int) -> bool:
        return vertex_id in self.virtual_vertex_id

    def delete_hyperedge(self, hyperedge_id: int, reserve_connectivity: bool):
        hyperedge = self.get_hyperedge_by_id(hyperedge_id)
        if not reserve_connectivity:
            for edge in hyperedge.edges:
                self.delete_edge(edge.id)
        else:
            vertices = hyperedge.vertices
            for i in range(len(vertices)):
                for j in range(i + 1, len(vertices)):
                    self.create_edge(
                        vertices[i], vertices[j], hyperedge.weight)
            for edge in hyperedge.edges:
                self.delete_edge(edge.id)
        self.id_hyperedge_map.pop(hyperedge_id)

    def get_relevant_hyperedges(self, vertex_id: int) -> List[HyperEdge]:
        relevant_hyperedges = []
        for hyperedge in self.id_hyperedge_map.values():
            if hyperedge.is_contain_vertex(vertex_id):
                relevant_hyperedges.append(hyperedge)
        return relevant_hyperedges

    def get_hyperedges(self) -> List[HyperEdge]:
        return list(self.id_hyperedge_map.values())
