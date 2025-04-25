from typing import Any, Dict, List
from tools.id import id_generator
from abc import ABC


VIRTUAL_KEY = "__VIRTUAL__"


@id_generator
class Vertex:
    """顶点类"""

    def __init__(self, key: Any, weight: float = 1):
        self.id = Vertex.get_next_id()
        self.key = key
        self.weight = weight
        self.data = {}  # 存储顶点的额外属性

    def __eq__(self, other: 'Vertex'):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

    def set_property(self, key: str, value: Any):
        self.data[key] = value

    def get_property(self, key: str) -> Any:
        return self.data.get(key)

    def to_string(self):
        if self.is_virtual():
            return f"{self.key}{self.id}__"
        return f"{self.key}"

    def is_virtual(self):
        return self.key == VIRTUAL_KEY


class VertexManager:
    def __init__(self):
        self.id_vertex_map: Dict[int, Vertex] = {}
        self.key_id_map: Dict[Any, int] = {}
        self.virtual_vertex_ids: List[int] = []

    def create_vertex(self, key: Any, weight: float = 1, *args, **kwargs):
        vertex = self.get_vertex_by_key(key)
        if vertex is None:
            vertex = Vertex(key, weight)
            for arg in args:
                if isinstance(arg, dict):
                    for key, value in arg.items():
                        vertex.set_property(key, value)
                else:
                    vertex.set_property(str(len(vertex.data)), arg)

            for key, value in kwargs.items():
                vertex.set_property(key, value)
            self.notify(vertex)
        return vertex

    def create_virtual_vertex(self):
        return self.create_vertex(VIRTUAL_KEY, 0)

    def notify(self, vertex: Vertex):
        self.id_vertex_map[vertex.id] = vertex
        if vertex.is_virtual():
            self.virtual_vertex_ids.append(vertex.id)
        else:
            self.key_id_map[vertex.key] = vertex.id

    def get_vertex_by_id(self, id: int) -> Vertex:
        return self.id_vertex_map[id]

    def get_vertex_by_key(self, key: Any) -> Vertex:
        if self.key_id_map.get(key) is None:
            return None
        return self.get_vertex_by_id(self.key_id_map[key])

    def clear(self):
        self.id_vertex_map.clear()

    def get_vertex_keys(self) -> List[Any]:
        """获取所有顶点的key列表

        Returns:
            List[Any]: 包含所有顶点key的列表
        """
        return list(self.key_id_map.keys())

    def get_verties(self) -> List[Vertex]:
        return list(self.id_vertex_map.values())

    def get_virtual_vertex_keys(self) -> List[Any]:
        return [vertex.key for vertex in self.id_vertex_map.values() if vertex.is_virtual()]
