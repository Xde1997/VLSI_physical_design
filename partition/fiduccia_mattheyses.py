# from base.graph import Graph
from base.hypergraph import HyperGraph
from .common import initial_partition
from .cell import CellManager
from base.vertex import Vertex
from base.edge import Edge
from .common import is_fixed_dict
import random
import copy
from typing import List, Tuple
from base.partition import Partition, SubPartition


def balance_criteria(graph: HyperGraph, r: float):
    vertices = graph.get_vertices()
    total_weight = sum(vertex.weight for vertex in vertices)
    max_weight = max(vertex.weight for vertex in vertices)
    lb = total_weight*r-max_weight
    ub = total_weight*r+max_weight
    return lb, ub


def calculate_balance(graph: HyperGraph, partition: Partition):
    subpartition = partition.subpartitions[0]
    return subpartition.get_total_weight(graph)


def fs(graph: HyperGraph, temp_partition: Partition, vertex: Vertex, cell_value: int):
    fs_value = 0
    edges = graph.get_relevant_edges(vertex.id)
    subpartition = temp_partition.get_subpartition(vertex.id)
    for edge in edges:
        # 检查该线网中是否只有当前顶点在指定划分中
        hyperedge = graph.get_hyperedge_contain_edge(edge.id)
        hyperedge_vertices = hyperedge.get_vertices()

        is_in = False
        for vertex_id in hyperedge_vertices:
            if vertex_id != vertex.id and vertex_id in subpartition.vertices:
                is_in = True
                break
        if not is_in:
            fs_value += 1
    return fs_value


def te(graph: HyperGraph, temp_partition: Partition, vertex: Vertex, cell_value: int):
    te_value = 0
    hyperedges = graph.get_relevant_hyperedges(vertex.id)
    subpartition = temp_partition.get_subpartition(vertex.id)
    for hyperedge in hyperedges:
        edges = hyperedge.get_edges()
        is_in = True
        for edge in edges:
            if edge not in subpartition.edges:
                is_in = False
                break
        if is_in:
            te_value += 1
    return te_value


def random_int(start: int, end: int) -> int:
    return random.randint(start, end)


def best_moves(order: List[Tuple[float, int]], balance_factors: List[int]) -> List[int]:
    best_moves = [[]]
    max_sum = float('-inf')
    current_sum = 0
    current_sequence = []

    for move in order:
        current_sum += move[0]
        current_sequence.append(move)

        if current_sum > max_sum:
            max_sum = current_sum
            best_moves = [current_sequence.copy()]
        elif current_sum == max_sum:
            best_moves.append(current_sequence.copy())

    # find best balance factor
    best_balance_factor = float('-inf')
    best_balance_moves = []
    for moves in best_moves:
        balance_factor = balance_factors[len(moves)-1]
        if balance_factor > best_balance_factor:
            best_balance_factor = balance_factor
            best_balance_moves = moves
    return best_balance_moves


def hash_gm(gm: dict[int, float]) -> tuple[int, float]:
    return tuple(gm.values())


def hash_gm_dict_add(gm_dict: dict, gm: dict[int, float]):
    key = hash_gm(gm)
    if key in gm_dict:
        gm_dict[key] += 1
    else:
        gm_dict[key] = 1


def max_gain(graph: HyperGraph, temp_partition: Partition, gm: dict[int, float], lb: float, ub: float, status: dict[int, bool]):
    max_gain_value = float('-inf')
    max_gain_vertex = []

    for vertex_id, gain in gm.items():
        subpartition = temp_partition.get_subpartition(vertex_id)
        weight = graph.get_vertex(vertex_id).weight
        current_balance = calculate_balance(graph, temp_partition)
        current_balance_a = 0
        if subpartition.id == 0:
            current_balance_a = current_balance-weight
        else:
            current_balance_a = current_balance+weight
        if current_balance_a < lb:
            continue
        if current_balance_a > ub:
            continue

        if not status[vertex_id] and gain > max_gain_value:
            max_gain_value = gain
            max_gain_vertex.clear()
            max_gain_vertex.append(vertex_id)
        elif not status[vertex_id] and gain == max_gain_value:
            max_gain_vertex.append(vertex_id)

    # for vertex_id in max_gain_vertex:
    #     subpartition = temp_partition.get_subpartition(vertex_id)
    #     weight = graph.get_vertex(vertex_id).weight
    #     if subpartition.get_total_weight(graph)-weight < lb:
    #         continue
    #     if subpartition.get_total_weight(graph)-weight > ub:
    #         continue
    #     return max_gain_value, vertex_id

    # if not found, return the first vertex
    return max_gain_value, max_gain_vertex[0]


def calculate_gain(graph: HyperGraph, temp_partition: Partition, vertex: Vertex, cell_value: int):
    return fs(graph, temp_partition, vertex, cell_value) - te(graph, temp_partition, vertex, cell_value)

# 后续再看第二轮为什么会出现问题
def fm(graph: HyperGraph, r: float):
    lb, ub = balance_criteria(graph, r)
    # initial_partition(graph, 2)
    partition = graph.partition
    gm_total = float('inf')

    CellManager.create_cell_values(graph.get_vertices())

    while gm_total > 0:
        temp_partition = copy.deepcopy(graph.partition)
        vertices = graph.get_vertices()
        i = 0
        gm = [{}]
        order = []
        status = {}
        hash_gm_map = dict()
        balance_factors = []
        for vertex in vertices:
            if vertex.is_virtual():
                continue
            cell_value = CellManager.get_cell_value(vertex)
            gm[i][vertex.id] = calculate_gain(
                graph, temp_partition, vertex, cell_value)
            status[vertex.id] = False
        while (not is_fixed_dict(status)):
            # if hash_gm(gm[i]) in hash_gm_map.keys() and hash_gm_map[hash_gm(gm[i])] > 2:
            #     break
            max_gain_value, max_gain_vertex = max_gain(
                graph, temp_partition, gm[i], lb, ub, status)
            order.append((max_gain_value, max_gain_vertex))

            subpartition = temp_partition.get_subpartition(max_gain_vertex)
            other_partitions = temp_partition.get_other_partitions(
                subpartition.id)
            other_partition = other_partitions[0]
            temp_partition.try_move(graph, max_gain_vertex,
                                    other_partition)
            balance_factors.append(calculate_balance(graph, temp_partition))
            print(f"after move {max_gain_vertex}")
            temp_partition.print(graph)
            status[max_gain_vertex] = True
            critical_nets = graph.get_relevant_hyperedges(max_gain_vertex)
            update_record = []
            hash_gm_dict_add(hash_gm_map, gm[-1])
            gm.append(copy.deepcopy(gm[-1]))
            i += 1
            for net in critical_nets:
                for vertex_id in net.get_vertices():
                    if not status[vertex_id] and vertex_id not in update_record:
                        # if vertex_id not in update_record:
                        update_vertex = graph.get_vertex(vertex_id)
                        if update_vertex.is_virtual():
                            continue
                        update_record.append(vertex_id)
                        gm[i][vertex_id] = calculate_gain(
                            graph, temp_partition, update_vertex, CellManager.get_cell_value(update_vertex))

        max_iters = best_moves(order, balance_factors)
        gm_total = sum(move[0] for move in max_iters)
        if gm_total > 0:
            for gain, vertex_id in max_iters:
                subpartition = partition.get_subpartition(vertex_id)
                other_partitions = partition.get_other_partitions(
                    subpartition.id)
                partition.try_move(graph, vertex_id,
                                   other_partitions[0])
    print("after fm")
    partition.print(graph)
