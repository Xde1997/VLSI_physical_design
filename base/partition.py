from typing import List, Set
# from .graph import Graph
from tools.id import id_generator


class Partition:
    """分区类"""

    def __init__(self):
        self.subpartitions: List['SubPartition'] = []
        self.cutset = CutSet()

    def get_subpartition(self, vertex_id: int) -> 'SubPartition':
        for subpartition in self.subpartitions:
            if vertex_id in subpartition.vertices:
                return subpartition
        return None

    def create_empty_subpartition(self) -> 'SubPartition':
        subpartition = SubPartition()
        self.subpartitions.append(subpartition)
        return subpartition

    def get_subpartition_by_id(self, subpartition_id: int) -> 'SubPartition':
        for subpartition in self.subpartitions:
            if subpartition.id == subpartition_id:
                return subpartition
        return None

    def get_other_partitions(self, subpartition_id: int) -> List[int]:
        other_partitions = []
        for subpartition in self.subpartitions:
            if subpartition.id != subpartition_id:
                other_partitions.append(subpartition.id)
        return other_partitions

    def get_relevant_edges(self, graph: 'Graph', vertex_id: int) -> tuple[List[int], List[int]]:
        """获取与指定顶点相关的所有边

        Args:
            vertex_id: 顶点ID

        Returns:
            与该顶点相关的所有边的ID列表
        """
        relevant_edges = []
        cutset_edges = []
        edges = graph.get_relevant_edges(vertex_id)
        subpartition = self.get_subpartition(vertex_id)
        if subpartition:
            for edge in edges:
                if edge.id in subpartition.edges:
                    relevant_edges.append(edge.id)
        for edge in edges:
            if edge.id in self.cutset.edges:
                cutset_edges.append(edge.id)

        return relevant_edges, cutset_edges

    def add_vertex(self, graph: 'Graph', vertex_id: int, partition_id: int):
        if self.get_subpartition(vertex_id):
            return
        edges = graph.get_relevant_edges(vertex_id)

        # 将顶点添加到指定分区
        subpartition = self.subpartitions[partition_id]
        subpartition.add_vertex(vertex_id)

        # 处理相关边
        for edge in edges:
            edge_id = edge.id
            other_vertex = edge.get_other_vertex(vertex_id)

            # 检查边的另一个端点是否在同一分区
            if other_vertex in subpartition.vertices:
                # 如果关联，将边加入子分区
                subpartition.add_edge(edge_id)
                if edge_id in self.cutset.edges:
                    self.cutset.remove_edge(edge_id)
            else:
                # 如果不关联，将边加入割集
                self.cutset.add_edge(edge_id)

    def remove_vertex(self, graph: 'Graph', vertex_id: int) -> tuple[List[int], List[int]]:
        relevant_edges = graph.get_relevant_edges(vertex_id)
        removed_relevant_edges = []
        removed_cutset_edges = []
        subpartition = self.get_subpartition(vertex_id)
        if subpartition:
            removed_relevant_edges = subpartition.remove_vertex(
                graph, vertex_id)
        for edge in relevant_edges:
            if edge.id in self.cutset.edges:
                self.cutset.remove_edge(edge.id)
                removed_cutset_edges.append(edge.id)
        return removed_relevant_edges, removed_cutset_edges

    def try_swap(self, graph: 'Graph', vertexa_id: int, vertexb_id: int):
        # 找到vertexa和vertexb所在的子分区
        subpartition_a = self.get_subpartition(vertexa_id)
        subpartition_b = self.get_subpartition(vertexb_id)

        if subpartition_a is None or subpartition_b is None:
            return False

        # 如果两个顶点在同一个子分区中，则不需要交换
        if subpartition_a.id == subpartition_b.id:
            return False

        removed_relevant_edges_a, removed_cutset_edges_a = self.remove_vertex(
            graph, vertexa_id)
        removed_relevant_edges_b, removed_cutset_edges_b = self.remove_vertex(
            graph, vertexb_id)

        self.add_vertex(graph, vertexa_id, subpartition_b.id)
        self.add_vertex(graph, vertexb_id, subpartition_a.id)

    def try_move(self, graph: 'Graph', vertex_id: int, partition_id: int):
        subpartition = self.get_subpartition(vertex_id)
        if subpartition is None:
            return False
        if partition_id == subpartition.id:
            return False
        subpartition.remove_vertex(graph, vertex_id)
        self.add_vertex(graph, vertex_id, partition_id)
        return True

    def print(self, graph: 'Graph'):
        """打印分区信息"""
        print(f"分区数量: {len(self.subpartitions)}")
        for i, subpartition in enumerate(self.subpartitions):
            print(f"子分区 {i}:")
            print(f"  顶点数量: {len(subpartition.vertices)}")
            print(f"  边数量: {len(subpartition.edges)}")
            subpartition.print(graph)
        print(f"割集边数量: {len(self.cutset.edges)}")
        self.cutset.print(graph)


@id_generator
class SubPartition:
    """分区类"""

    def __init__(self):
        self.vertices: Set[int] = set()
        self.edges: Set[int] = set()
        self.id: int = SubPartition.get_next_id()

    def add_edge(self, edge_id):
        self.edges.add(edge_id)

    def add_vertex(self, vertex_id):
        self.vertices.add(vertex_id)

    def exist_vertex(self, vertex_id):
        return vertex_id in self.vertices

    def exist_edge(self, edge_id):
        return edge_id in self.edges

    def remove_vertex(self, graph: 'Graph', vertex_id) -> List[int]:
        relevant_edges = []
        self.vertices.remove(vertex_id)
        edges = graph.get_relevant_edges(vertex_id)
        for edge in edges:
            if edge.id in self.edges:
                self.edges.remove(edge.id)
                relevant_edges.append(edge.id)
        return relevant_edges

    def get_total_weight(self, graph: 'Graph'):
        return sum(graph.get_vertex(vertex).weight for vertex in self.vertices)

    def print(self, graph: 'Graph'):
        """打印子分区信息"""
        print(
            f"  顶点: {([graph.get_vertex(v).to_string() for v in self.vertices])}")
        print(
            f"  边: {([graph.get_edge_by_id(e).to_string(graph) for e in self.edges])}")


class CutSet:
    """割集类"""

    def __init__(self):
        self.edges: Set[int] = set()

    def add_edge(self, edge_id):
        self.edges.add(edge_id)

    def exist_edge(self, edge_id):
        return edge_id in self.edges

    def remove_edge(self, edge_id):
        self.edges.remove(edge_id)

    def print(self, graph: 'Graph'):
        """打印割集信息"""
        print(
            f"割集边: {([graph.get_edge_by_id(e).to_string(graph) for e in self.edges])}")
