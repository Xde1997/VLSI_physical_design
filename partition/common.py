from base.graph import Graph
from base.partition import Partition, SubPartition
from typing import List, Dict
import random


def initial_partition(graph: Graph, n: int) -> Graph:
    """
    将图随机分成n个分区

    Args:
        graph: 要分区的图
        n: 分区数量

    Returns:
        dict: 顶点到分区号的映射字典
    """

    # 获取所有顶点
    vertices = graph.get_vertices()

    # 随机打乱顶点顺序
    random.shuffle(vertices)

    # 计算每个分区应该包含的顶点数量
    partition_size = len(vertices) // n
    remainder = len(vertices) % n

    # 创建分区映射
    partition = Partition()
    partitions = List[SubPartition()]

    current_index = 0

    # 分配顶点到各个分区
    for i in range(n):
        # 处理余数，将多余的顶点分配到前面的分区
        size = partition_size + (1 if i < remainder else 0)
        subpartition = SubPartition()
        subpartition.id = i

        # 分配顶点
        for j in range(size):
            if current_index < len(vertices):
                vertex = vertices[current_index]
                subpartition.add_vertex(vertex.id)
                current_index += 1

        # 保存边的关系
        for vertex_id in subpartition.vertices:
            neighbors = graph.get_neighbors(vertex_id)
            for neighbor in neighbors:
                edge_id = graph.get_edge(vertex_id, neighbor.id).id
                if neighbor.id not in subpartition.vertices:
                    # 如果邻居在另一个分区，则这条边属于割集
                    partition.cutset.add_edge(edge_id)
                else:
                    subpartition.add_edge(edge_id)

        partition.subpartitions.append(subpartition)

    graph.partition = partition
    return graph


def is_fixed(status: List[int]) -> bool:
    return all(x == 1 for x in status)


def is_fixed_dict(status: Dict[int, bool]) -> bool:
    return all(x == True for x in status.values())
