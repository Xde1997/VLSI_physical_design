import copy
from typing import List
from base.graph import Graph
import random
from base.partition import Partition, SubPartition
from .common import initial_partition, is_fixed

def dv(graph: Graph, partition: Partition, vertex_id: int):
    relevant_edges, cutset_edges = partition.get_relevant_edges(graph,
                                                                vertex_id)
    sum_rele = 0
    for edgeid in relevant_edges:
        edge = graph.get_edge_by_id(edgeid)
        sum_rele += edge.weight
    sum_cutset = 0
    for edgeid in cutset_edges:
        edge = graph.get_edge_by_id(edgeid)
        sum_cutset += edge.weight
    return sum_cutset-sum_rele


def connection_weight(graph: Graph, vertexa_id: int, vertexb_id: int) -> float:
    edge = graph.get_edge(vertexa_id, vertexb_id)
    if edge is None:
        return 0
    return edge.weight


def max_gain(graph: Graph, partition: Partition, status: List[int]) -> tuple[float, int, int]:
    partition_a = partition.subpartitions[0]
    partition_b = partition.subpartitions[1]
    max_gi = float('-inf')
    ai = -1
    bi = -1
    for a in partition_a.vertices:
        for b in partition_b.vertices:
            if status[a] == 1 or status[b] == 1:
                continue
            gi = dv(graph, partition, a)+dv(graph, partition, b) - \
                2*connection_weight(graph, a, b)
            if max_gi < gi:
                max_gi = gi
                ai = a
                bi = b
    return max_gi, ai, bi


def get_max_two_d_node(partition_a: list[int], partition_b: list[int], status: List[int], d: List[int]) -> tuple[int, int]:
    max_a = float('-inf')
    max_b = float('-inf')
    idx_a = -1
    idx_b = -1

    for i in partition_a:
        if status[i] == 1:
            continue
        if d[i] > max_a:
            max_a = d[i]
            idx_a = i

    for i in partition_b:
        if status[i] == 1:
            continue
        if d[i] > max_b:
            max_b = d[i]
            idx_b = i

    return idx_a, idx_b


def hash_partition(partition):
    a_ids = sorted([v for v in partition.subpartitions[0].vertices])
    b_ids = sorted([v for v in partition.subpartitions[1].vertices])
    return tuple(a_ids), tuple(b_ids)


def get_max_gain_total(gm: List[float]) -> tuple[int, float]:
    max_sum = float('-inf')
    current_sum = 0
    max_index = 0
    for i in range(len(gm)):
        current_sum += gm[i]
        if current_sum > max_sum:
            max_sum = current_sum
            max_index = i
    return max_index, max_sum


def kl(graph: Graph) -> Graph:

    graph = initial_partition(graph, 2)

    partition = graph.partition
    print("before kl")
    partition.print(graph)

    gm_total = float('inf')
    max_gm_iter = 0
    seen_partitions = set()
    vertices = graph.get_vertices()
    # 0为free节点
    i = 0
    while (gm_total > 0):
        print(f"gm_total: {gm_total}")
        temp_partition = copy.deepcopy(partition)
        a = temp_partition.subpartitions[0]
        b = temp_partition.subpartitions[1]

        order = []
        status = [0] * len(vertices)
        gm = []
        D = [0]*len(vertices)
        for vertex in vertices:
            D[vertex.id] = dv(graph, temp_partition, vertex.id)
        while (not is_fixed(status)):
            # ai, bi = get_max_two_d_node(a.vertices, b.vertices, status, D)
            # gi = D[ai]+D[bi]-2*connection_weight(graph, ai, bi)
            gi, ai, bi = max_gain(graph, temp_partition, status)
            gm.append(gi)
            # 设置为fixed

            order.append((gi, ai, bi))
            temp_partition.try_swap(graph, ai, bi)
            status[ai] = 1
            status[bi] = 1
            connneted_vertices = []
            connneted_vertices.extend(graph.get_neighbors(ai))
            connneted_vertices.extend(graph.get_neighbors(bi))
            for vertex in connneted_vertices:
                D[vertex.id] = dv(graph, temp_partition, vertex.id)
        max_index, gm_total = get_max_gain_total(gm)

        if gm_total > 0:
            for i in range(max_index+1):
                gi, ai, bi = order[i]
                partition.try_swap(graph, ai, bi)
            partition_hash = hash_partition(partition)
            if partition_hash in seen_partitions:
                print("Detected repeating partition. Exiting to avoid infinite loop.")
                break
            seen_partitions.add(partition_hash)

        i = i+1
        # # gm_total = sum(gm)
        # i = i+1
        # if gm_total > 0:
        #     partition = copy.deepcopy(temp_partition)
    print("after kl")
    partition.print(graph)
    print(f"total iteration: {i}")


def extend_kl_unequal(graph: Graph) -> Graph:
    graph = initial_partition(graph, 2)

    partition = graph.partition
    print("before kl")
    partition.print(graph)

    gm_total = float('inf')
    seen_partitions = set()
    vertices = graph.get_vertices()
    i = 0

    while gm_total > 0:
        print(f"\nIteration {i}, gm_total: {gm_total}")

        temp_partition = copy.deepcopy(partition)
        a = temp_partition.subpartitions[0]
        b = temp_partition.subpartitions[1]

        order = []
        status = [0] * len(vertices)
        gm = []
        D = [0] * len(vertices)

        for vertex in vertices:
            D[vertex.id] = dv(graph, temp_partition, vertex.id)

        # 限制最多交换 min(len(A), len(B)) 对
        max_swap_count = min(len(a.vertices), len(b.vertices))
        swap_count = 0

        while not is_fixed(status) and swap_count < max_swap_count:
            gi, ai, bi = max_gain(graph, temp_partition, status)
            gm.append(gi)
            order.append((gi, ai, bi))

            temp_partition.try_swap(graph, ai, bi)
            status[ai] = 1
            status[bi] = 1

            connected_vertices = graph.get_neighbors(
                ai) + graph.get_neighbors(bi)
            for vertex in connected_vertices:
                D[vertex.id] = dv(graph, temp_partition, vertex.id)

            swap_count += 1

        max_index, gm_total = get_max_gain_total(gm)

        if gm_total > 0:
            for j in range(max_index + 1):
                gi, ai, bi = order[j]
                partition.try_swap(graph, ai, bi)

            partition_hash = hash_partition(partition)
            if partition_hash in seen_partitions:
                print("Detected repeating partition. Exiting to avoid infinite loop.")
                break
            seen_partitions.add(partition_hash)

        i += 1

    print("\nafter kl_unequal")
    partition.print(graph)
    print(f"total iteration: {i}")
    return graph


def kl_weighted(graph: Graph) -> Graph:
    enforce_self_loop_inf(graph)
    graph = initial_partition(graph, 2)
    partition = graph.partition
    print("before kl_weighted")
    partition.print(graph)

    seen_partitions = set()
    vertices = graph.get_vertices()
    i = 0
    gm_total = float('inf')

    while gm_total > 0:
        print(f"\nIteration {i}, gm_total: {gm_total}")
        temp_partition = copy.deepcopy(partition)
        a = temp_partition.subpartitions[0]
        b = temp_partition.subpartitions[1]

        order = []
        status = [0] * len(vertices)
        gm = []
        D = [0] * len(vertices)

        for vertex in vertices:
            D[vertex.id] = dv(graph, temp_partition, vertex.id)

        max_swap_count = min(
            sum(v.weight for v in a.vertices),
            sum(v.weight for v in b.vertices)
        ) // get_min_cell_weight(vertices)  # 按最小元胞单位限制
        swap_count = 0

        while not is_fixed(status) and swap_count < max_swap_count:
            gi, ai, bi = max_gain(graph, temp_partition, status)

            # 检查交换是否会打破平衡（允许一定范围的浮动）
            if not can_swap_by_weight(temp_partition, ai, bi):
                status[ai] = 1
                status[bi] = 1
                continue

            gm.append(gi)
            order.append((gi, ai, bi))

            temp_partition.try_swap(graph, ai, bi)
            status[ai] = 1
            status[bi] = 1

            neighbors = graph.get_neighbors(ai) + graph.get_neighbors(bi)
            for v in neighbors:
                D[v.id] = dv(graph, temp_partition, v.id)

            swap_count += 1

        max_index, gm_total = get_max_gain_total(gm)

        if gm_total > 0:
            for j in range(max_index + 1):
                gi, ai, bi = order[j]
                partition.try_swap(graph, ai, bi)

            h = hash_partition(partition)
            if h in seen_partitions:
                print("Detected repeating partition. Exiting.")
                break
            seen_partitions.add(h)

        i += 1

    print("\nafter kl_weighted")
    partition.print(graph)
    print(f"total iteration: {i}")
    return graph
