from collections.abc import Sequence
from .graph import Graph, ListGraph, MatrixGraph
from .successor import SuccessorGraph
from .traversal import _dfs_list, _dfs_matrix, _dfs_successor


# COUNT ISLANDS
def count_islands(graph: Graph) -> int:
    """returns the number of distinct islands in a graph"""

    if isinstance(graph, ListGraph):
        return _count_islands_list(graph)
    if isinstance(graph, MatrixGraph):
        return _count_islands_matrix(graph)
    if isinstance(graph, SuccessorGraph):
        return _count_islands_successor(graph)

    raise NotImplementedError(f"count_islands not supported for '{type(graph).__name__}'")

def _count_islands_list(graph: ListGraph) -> int:
    """helper function of count_islands for ListGraphs"""

    visited = [False] * graph.order
    count = 0
    for i in range(graph.order):
        if not visited[i]:
            _dfs_list(graph, i, visited)
            count += 1

    return count

def _count_islands_matrix(graph: MatrixGraph) -> int:
    """helper function of count_islands for MatrixGraphs"""

    visited = [False] * graph.order
    count = 0
    for i in range(graph.order):
        if not visited[i]:
            _dfs_matrix(graph, i, visited)
            count += 1

    return count

def _count_islands_successor(graph: SuccessorGraph) -> int:
    """helper function of count_islands for SuccessorGraphs"""

    visited = [False] * graph.order
    count = 0
    for i in range(graph.order):
        if not visited[i]:
            _dfs_successor(graph, i, visited)
            count += 1

    return count

# SPLIT
def split(graph: Graph) -> Sequence[Graph | SuccessorGraph]:
    """separate all islands of a graph and returns a list of these islands (as distinct graph objects of the same variant)"""

    if isinstance(graph, ListGraph):
        return _split_list(graph)
    if isinstance(graph, MatrixGraph):
        return _split_matrix(graph)
    if isinstance(graph, SuccessorGraph):
        return _split_successor(graph)

    raise NotImplementedError(f"split not supported for '{type(graph).__name__}'")

def _split_list(graph: ListGraph) -> Sequence[ListGraph]:
    """helper function of split for ListGraphs"""

    visited = [False] * graph.order
    result = []

    for i in range(graph.order):
        if not visited[i]:
            new_graph = ListGraph(1)
            vertex_map = {i: 0}
            _split_list_dfs(graph, visited, new_graph, vertex_map, i)
            result.append(new_graph)

    return result

def _split_list_dfs(graph: ListGraph, visited: list[bool], new_graph: ListGraph, vertex_map: dict[int, int],
                    current: int) -> None:
    """helper function of _split_list"""

    visited[current] = True

    for e in graph.adj[current]:
        if e.dest not in vertex_map:
            vertex_map[e.dest] = len(vertex_map)
            new_graph.add_edge(vertex_map[e.origin], vertex_map[e.dest], e.weight)

        if not visited[e.dest]:
            _split_list_dfs(graph, visited, new_graph, vertex_map, e.dest)

def _split_matrix(graph: MatrixGraph) -> Sequence[MatrixGraph]:
    """helper function of split for MatrixGraphs"""

    visited = [False] * graph.order
    result = []

    for i in range(graph.order):
        if not visited[i]:
            new_graph = MatrixGraph(1)
            vertex_map = {i: 0}
            _split_matrix_dfs(graph, visited, new_graph, vertex_map, i)
            result.append(new_graph)

    return result

def _split_matrix_dfs(graph: MatrixGraph, visited: list[bool], new_graph: MatrixGraph, vertex_map: dict[int, int],
                      current: int) -> None:
    """helper function of _split_matrix"""

    visited[current] = True

    for i, e in enumerate(graph.adj[current]):
        if e != graph.default_value:
            if i not in vertex_map:
                vertex_map[i] = len(vertex_map)
                new_graph.add_edge(vertex_map[current], vertex_map[i], e)

            if not visited[i]:
                _split_matrix_dfs(graph, visited, new_graph, vertex_map, i)

def _split_successor(graph: SuccessorGraph) -> Sequence[SuccessorGraph]:
    """helper function of split for SuccessorGraphs"""

    visited = [False] * graph.order
    result = []

    for i in range(graph.order):
        if not visited[i]:
            new_graph = SuccessorGraph(1)
            vertex_map = {i: 0}
            _split_successor_dfs(graph, visited, new_graph, vertex_map, i)
            result.append(new_graph)

    return result

def _split_successor_dfs(graph: SuccessorGraph, visited: list[bool], new_graph: SuccessorGraph,
                         vertex_map: dict[int, int], current: int) -> None:
    """helper function of _split_successor"""

    visited[current] = True

    e = graph.adj[current]
    if e.dest is not None:
        if e.dest not in vertex_map:
            vertex_map[e.dest] = len(vertex_map)
            new_graph.add_edge(vertex_map[e.origin], vertex_map[e.dest], e.weight)

        if not visited[e.dest]:
            _split_successor_dfs(graph, visited, new_graph, vertex_map, e.dest)