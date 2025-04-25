from typing import List

import numpy as np

from base.point import Point2D


class FloorplanModule:
    def __init__(self, name: str, area: float, hw_ratio: List[float]):
        self.name = name
        self.area = area
        self.hw_ratio = hw_ratio
        self.offset: Point2D
        self.length: float
        self.width: float
        self.status: bool = False

        self.terminal_list: List[Point2D]

    def initialize(self):
        pass

    def get_centroid(self):
        if self.status:
            return Point2D(self.offset.x + self.length / 2, self.offset.y + self.width / 2)
        else:
            return None

# 将modules使用最小面积进行floorplan


class Floorplan:
    def __init__(self):
        self.modules = []
        self.border_lb: Point2D
        self.length: float
        self.width: float
        self.nets = []
        self.blocks = []
        # self.nets_to_blocks = []
        # self.nets_to_modules = []
        self.connections = np.array([[]])

        # 是否已经完成floorplan
        self.status = False

    def add_module(self, module: FloorplanModule):
        self.modules.append(module)

    def run(self):
        pass

    # using connections matrix
    def total_net_length(self):
        total_length = 0
        for i in range(len(self.modules)):
            for j in range(i + 1, len(self.modules)):
                if self.modules[i].status and self.modules[j].status:
                    centroid1 = self.get_centroid(self.modules[i])
                    centroid2 = self.get_centroid(self.modules[j])
                    d_ij = np.sum(np.abs(centroid1 - centroid2))
                    total_length += self.connections[i, j] * d_ij
        return total_length

    # using mst
    def total_net_length_mst(self):
        pass

    def estimate_floorplan(self, alpha: float):
        return alpha*self.area+(1-alpha)*self.total_net_length()
