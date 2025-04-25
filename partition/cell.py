from base.vertex import Vertex
from typing import List
import math


CELL_VALUE = 'cell_value'  # 用于存储顶点元胞值的属性键


class CellManager:
    def __init__(self):
        pass

    @staticmethod
    def create_cell_values(vertex_ids: List[Vertex]):
        min_weight = float('inf')
        for vertex in vertex_ids:
            if vertex.weight == 0:
                continue
            if vertex.weight < min_weight:
                min_weight = vertex.weight
        for vertex in vertex_ids:
            ceil = math.ceil(vertex.weight/min_weight)
            vertex.set_property(CELL_VALUE, ceil)

    @staticmethod
    def get_cell_value(vertex: Vertex):
        return vertex.get_property(CELL_VALUE)
