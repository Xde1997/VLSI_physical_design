from typing import List

import numpy as np

from base.point import Point2D


class FloorplanModule:
    def __init__(self, name: str, offset: Point2D, length: float, width: float):
        self.name = name
        self.length = length
        self.width = width
        self.offset = offset
        self.status: bool = False

        self.terminal_list: List[Point2D]

    def initialize(self):
        self.status = True

    def get_centroid(self):
        if self.status:
            return Point2D(self.offset.x + self.length / 2, self.offset.y + self.width / 2)
        else:
            return None

    def in_x_range(self, x: float):
        return self.offset.x <= x and x <= self.offset.x + self.length

    def in_y_range(self, y: float):
        return self.offset.y <= y and y <= self.offset.y + self.width


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
        self.reconstruct()

    def run(self):
        pass

    def get_lb(self):
        return self.border_lb

    def get_length(self):
        return self.length

    def get_width(self):
        return self.width

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

    def reconstruct(self):
        x_min = min([module.offset.x for module in self.modules])
        y_min = min([module.offset.y for module in self.modules])
        x_max = max(
            [module.offset.x + module.length for module in self.modules])
        y_max = max(
            [module.offset.y + module.width for module in self.modules])
        self.border_lb = Point2D(x_min, y_min)
        self.length = x_max - x_min
        self.width = y_max - y_min
    # using mst

    def total_net_length_mst(self):
        pass

    def estimate_floorplan(self, alpha: float):
        return alpha*self.area+(1-alpha)*self.total_net_length()
