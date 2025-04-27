from base.graph import DirectedGraph
from .floorplan import Floorplan, FloorplanModule
from base.point import Point2D
from typing import List
from tools.math import manhattan_distance


def is_interval_overlap(interval1: List[float], interval2: List[float]) -> bool:
    """
    判断两个区间是否相交

    Args:
        interval1: 第一个区间 [left, right]
        interval2: 第二个区间 [left, right]

    Returns:
        bool: 如果相交返回True,否则返回False
    """
    return not (interval1[1] <= interval2[0] or interval2[1] <= interval1[0])


class ConstrainGraphPair:
    def __init__(self, floorplan: Floorplan):
        if not floorplan.status:
            raise ValueError("Floorplan is not initialized")
        self.vcg = DirectedGraph()
        self.hcg = DirectedGraph()
        self.create_vcg(floorplan)
        self.create_hcg(floorplan)

        # self.hcg.add_vertex("s", 0)
        # self.hcg.add_vertex("t", 0)

    def create_vcg(self, floorplan: Floorplan):
        lb = floorplan.get_lb()
        bottom = lb.y
        top = lb.x+floorplan.get_width()
        length = floorplan.get_length()
        virtual_module_s = FloorplanModule(
            "s", Point2D(lb.x, bottom-1), length, 1)
        virtual_module_t = FloorplanModule(
            "t", Point2D(lb.x, top), length, 1)
        virtual_module_s.initialize()
        virtual_module_t.initialize()

        total_modules = [virtual_module_s]+floorplan.modules + \
            [virtual_module_t]

        for module in total_modules:
            self.vcg.add_coord_vertex(module.name, 0, module.get_centroid())

        total_modules.sort(key=lambda x: x.offset.y)

        for i in range(len(total_modules)-1):
            module_bottom = total_modules[i].offset.y
            module_top = module_bottom+total_modules[i].width
            module_left = total_modules[i].offset.x
            module_right = module_left+total_modules[i].length
            x_range = [module_left, module_right]
            for j in range(i+1, len(total_modules)):
                if total_modules[j].offset.y <= module_bottom:
                    continue
                j_left = total_modules[j].offset.x
                j_right = j_left+total_modules[j].length
                if is_interval_overlap(x_range, [j_left, j_right]):
                    vertex_i = self.vcg.get_vertex_by_key(
                        total_modules[i].name)
                    vertex_j = self.vcg.get_vertex_by_key(
                        total_modules[j].name)
                    self.vcg.add_edge(vertex_i.id, vertex_j.id, manhattan_distance(
                        vertex_i.coord, vertex_j.coord))
        self.pruning(self.vcg)

    def create_hcg(self, floorplan: Floorplan):
        lb = floorplan.get_lb()
        left = lb.x
        right = lb.x + floorplan.get_length()
        width = floorplan.get_width()

        # 创建虚拟模块s和t
        virtual_module_s = FloorplanModule(
            "s", Point2D(left-1, lb.y), 1, width)
        virtual_module_t = FloorplanModule(
            "t", Point2D(right, lb.y), 1, width)
        virtual_module_s.initialize()
        virtual_module_t.initialize()

        total_modules = [virtual_module_s] + \
            floorplan.modules + [virtual_module_t]

        # 添加顶点
        for module in total_modules:
            self.hcg.add_coord_vertex(module.name, 0, module.get_centroid())

        # 按x坐标排序
        total_modules.sort(key=lambda x: x.offset.x)

        # 添加边
        for i in range(len(total_modules)-1):
            module_left = total_modules[i].offset.x
            module_right = module_left + total_modules[i].length
            module_bottom = total_modules[i].offset.y
            module_top = module_bottom + total_modules[i].width
            y_range = [module_bottom, module_top]

            for j in range(i+1, len(total_modules)):
                if total_modules[j].offset.x <= module_left:
                    continue
                j_bottom = total_modules[j].offset.y
                j_top = j_bottom + total_modules[j].width
                if is_interval_overlap(y_range, [j_bottom, j_top]):
                    vertex_i = self.hcg.get_vertex_by_key(
                        total_modules[i].name)
                    vertex_j = self.hcg.get_vertex_by_key(
                        total_modules[j].name)
                    self.hcg.add_edge(vertex_i.id, vertex_j.id, 1)
        self.pruning(self.hcg)

    def pruning(self, graph: DirectedGraph):
        total_edges = graph.get_edges()
        for vertex in graph.get_vertices():
            edges = graph.get_revelant_edges_start_by(vertex.id)
            relevant_vertices = [vertex.id]
            for edge in edges:
                other_vertex = edge.get_other_vertex(vertex.id)
                relevant_vertices.append(other_vertex)
            for edge in total_edges:
                if edge not in edges and edge.vertices[0] in relevant_vertices and edge.vertices[1] in relevant_vertices:
                    delete_edge_1 = graph.get_edge(vertex.id, edge.vertices[0])
                    delete_edge_2 = graph.get_edge(vertex.id, edge.vertices[1])
                    if delete_edge_2 is None and delete_edge_1 is None:
                        # raise ValueError("No edge to delete")
                        pass
                    elif delete_edge_1 is None:
                        # graph.delete_edge(delete_edge_2.id)
                        pass
                    elif delete_edge_2 is None:
                        # graph.delete_edge(delete_edge_1.id)
                        pass
                    else:
                        graph.delete_edge(delete_edge_1.id if delete_edge_1.weight >
                                          delete_edge_2.weight else delete_edge_2.id)

    def print(self):
        self.vcg.print()
        self.hcg.print()
