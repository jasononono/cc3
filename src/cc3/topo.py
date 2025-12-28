from collections import deque
from collections.abc import Sequence
from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph
from .flags import GraphError


def topo_sort(graph: Graph, safe = False) -> Sequence[int]:
    """topologically sort a directed graph into an array

    if safe is True, then an unsortable graph (contains cycle) will raise an error."""

    if isinstance(graph, ListGraph):
        result = _topo_sort_list(graph)
    elif isinstance(graph, MatrixGraph):
        result = _topo_sort_matrix(graph)
    elif isinstance(graph, SuccessorGraph):
        result = _topo_sort_successor(graph)
    else:
        raise NotImplementedError(f"topological sorting not supported for '{type(graph).__name__}'")

    if safe and len(result) != graph.order:
        raise GraphError("graph cannot be topologically sorted (contains cycle)")
    return result

def _topo_sort_list(graph: ListGraph) -> Sequence[int]:
    """helper function of topo_sort for ListGraphs"""

    if not graph.directed:
        raise GraphError("topological sorting not supported for undirected graphs")

    in_degree = [0] * graph.order
    for n in graph.adj:
        for e in n:
            in_degree[e.dest] += 1

    queue = deque()
    result = []
    for n in range(graph.order):
        if in_degree[n] == 0:
             queue.append(n)

    while len(queue) > 0:
        current = queue.popleft()
        result.append(current)

        for e in graph.adj[current]:
            in_degree[e.dest] -= 1
            if in_degree[e.dest] == 0:
                queue.append(e.dest)

    return result

def _topo_sort_matrix(graph: MatrixGraph) -> Sequence[int]:
    """helper function of topo_sort for ListGraphs"""

    if not graph.directed:
        raise GraphError("topological sorting not supported for undirected graphs")

    in_degree = [0] * graph.order
    for n in graph.adj:
        for i, e in enumerate(n):
            if e != graph.default_value:
                in_degree[i] += 1

    queue = deque()
    result = []
    for n in range(graph.order):
        if in_degree[n] == 0:
            queue.append(n)

    while len(queue) > 0:
        current = queue.popleft()
        result.append(current)

        for i, e in enumerate(graph.adj[current]):
            if e != graph.default_value:
                in_degree[i] -= 1
                if in_degree[i] == 0:
                    queue.append(i)

    return result

def _topo_sort_successor(graph: SuccessorGraph) -> Sequence[int]:
    """helper function of topo_sort for SuccessorGraphs"""

    in_degree = [0] * graph.order
    for n in graph.adj:
        if n is not None:
            in_degree[n.dest] += 1

    queue = deque()
    result = []
    for n in range(graph.order):
        if in_degree[n] == 0:
            queue.append(n)

    while len(queue) > 0:
        current = queue.popleft()
        result.append(current)

        e = graph.adj[current]
        if e is not None:
            in_degree[e.dest] -= 1
            if in_degree[e.dest] == 0:
                queue.append(e.dest)

    return result