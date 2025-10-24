from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph


# CYCLE DETECTION
def has_cycle(graph: Graph | SuccessorGraph) -> bool:
    """returns a boolean indicating whether there is a cycle in a graph"""

    if isinstance(graph, SuccessorGraph):
        return has_cycle_successor(graph)
    if graph.directed:
        return has_cycle_directed(graph)
    return has_cycle_undirected(graph)


# UNDIRECTED
def has_cycle_undirected(graph: Graph) -> bool:
    """returns a boolean indicating whether there is a cycle in an undirected graph"""

    visited = [False] * graph.order
    function = _has_cycle_undirected_list if isinstance(graph, ListGraph) else _has_cycle_undirected_matrix

    for n in range(len(visited)):
        if not visited[n] and function(graph, n, -1, visited):
            return True
    return False


def _has_cycle_undirected_list(graph: ListGraph, current: int, parent: int, visited: list[bool]) -> bool:
    """helper function of has_cycle_undirected for ListGraphs"""

    visited[current] = True
    for e in graph.adj[current]:
        if e.dest == parent:
            continue
        if visited[e.dest] or _has_cycle_undirected_list(graph, e.dest, current, visited):
            return True
    return False


def _has_cycle_undirected_matrix(graph: MatrixGraph, current: int, parent: int, visited: list[bool]) -> bool:
    """helper function of has_cycle_undirected for MatrixGraphs"""

    visited[current] = True
    for e in range(graph.order):
        if graph.adj[current][e] == graph.default_value or e == parent:
            continue
        if visited[e] or _has_cycle_undirected_matrix(graph, e, current, visited):
            return True
    return False


# DIRECTED GRAPH
def has_cycle_directed(graph: Graph):
    """returns a boolean indicating whether there is a cycle in a directed graph"""

    visited = [0] * graph.order
    function = _has_cycle_directed_list if isinstance(graph, ListGraph) else _has_cycle_directed_matrix

    for n in range(graph.order):
        if not visited[n] and function(graph, n, visited):
            return True
    return False


def _has_cycle_directed_list(graph: ListGraph, current: int, visited: list[int]) -> bool:
    """helper function of has_cycle_directed for ListGraphs"""

    visited[current] = 1
    for e in graph.adj[current]:
        if visited[e.dest] == 1 or (not visited[e.dest] and _has_cycle_directed_list(graph, e.dest, visited)):
            return True

    visited[current] = 2
    return False


def _has_cycle_directed_matrix(graph: MatrixGraph, current: int, visited: list[int]) -> bool:
    """helper function of has_cycle_directed for MatrixGraphs"""

    visited[current] = 1
    for e in range(graph.order):
        if graph.adj[current][e] == graph.default_value:
            continue
        if visited[e] == 1 or (not visited[e] and _has_cycle_directed_matrix(graph, e, visited)):
            return True

    visited[current] = 2
    return False


# SUCCESSOR GRAPH
def has_cycle_successor(graph: SuccessorGraph) -> bool:
    """returns a boolean indicating whether there is a cycle in a successor graph"""

    visited = [0] * graph.order

    for n in range(graph.order):
        if not visited[n] and _has_cycle_successor_dfs(graph, n, visited):
            return True
    return False


def _has_cycle_successor_dfs(graph: SuccessorGraph, current: int, visited: list[int]) -> bool:
    """helper function of has_cycle_successor"""

    visited[current] = 1

    if graph.out_degree(current):
        e = graph.adj[current].dest
        if visited[e] == 1 or (not visited[e] and _has_cycle_successor_dfs(graph, e, visited)):
            return True

    visited[current] = 2
    return False