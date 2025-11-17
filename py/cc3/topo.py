from collections import deque
from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph


def sort(graph: Graph) -> Sequence[int]:
    if isinstance(graph, ListGraph):
        return _sort_list(graph)
    if isinstance(graph, MatrixGraph):
        return _sort_matrix(graph)
    if isinstance(graph, SuccessorGraph):
        return _sort_successor(graph)
    
    raise NotImplementedError(f"topological sorting not supported for '{type(graph).__name__}'")

def _sort_list(graph: ListGraph) -> Sequence[int]:
    if not graph.directed:
        raise TypeError("topological sorting not supported on undirected graphs")

    adj = graph.get_data()
    in_degree = [0] * graph.order
    for n in graph:
        for e in n:
            in_degree[e.dest] += 1

    queue = deque()
    result = []
    for n in range(graph.order):
        if in_degree[n] == 0:
             queue.append(n)

    while len(q) > 0:
        current = queue.popleft()
        result.append(current)

        for i in graph.adj[current]:
            in_degree[i] -= 1
            if in_degree[i] == 0:
                queue.append(i)