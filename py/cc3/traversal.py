from collections import deque
from collections.abc import Sequence
from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph


# BFS
def bfs(graph: Graph | SuccessorGraph, anchor = 0) -> Sequence[int]:
    """run the breadth-first search algorithm on a graph

    returns an array indicating all nodes' distance/depth from anchor. A value of -1 means that the node cannot be reached"""

    if graph.order == 0:
        raise IndexError("cannot run bfs on empty graph")
    if not 0 <= anchor < graph.order:
        raise IndexError("vertex does not exist in graph")

    if isinstance(graph, ListGraph):
        return _bfs_list(graph, anchor)
    elif isinstance(graph, MatrixGraph):
        return _bfs_matrix(graph, anchor)
    elif isinstance(graph, SuccessorGraph):
        return _bfs_successor(graph, anchor)

    raise NotImplementedError(f"bfs not supported for '{type(graph).__name__}'")


def _bfs_list(graph: ListGraph, anchor = 0) -> Sequence[int]:
    """bfs helper function for list graphs"""

    queue = deque()
    visited = [False] * graph.order
    dist = [-1] * graph.order

    queue.append(anchor)
    visited[anchor] = True
    dist[anchor] = 0

    while len(queue) > 0:
        current = queue.popleft()

        for e in graph.adj[current]:
            if not visited[e.dest]:
                queue.append(e.dest)
                visited[e.dest] = True
                dist[e.dest] = dist[current] + 1

    return dist


def _bfs_matrix(graph: MatrixGraph, anchor = 0) -> Sequence[int]:
    """bfs helper function for matrix graphs"""

    queue = deque()
    visited = [False] * graph.order
    dist = [-1] * graph.order

    queue.append(anchor)
    visited[anchor] = True
    dist[anchor] = 0

    while len(queue) > 0:
        current = queue.popleft()

        for i, e in enumerate(graph.adj[current]):
            if e != graph.default_value and not visited[i]:
                queue.append(i)
                visited[i] = True
                dist[i] = dist[current] + 1

    return dist


def _bfs_successor(graph: SuccessorGraph, anchor = 0) -> Sequence[int]:
    """bfs helper function for successor graphs"""

    queue = deque()
    visited = [False] * graph.order
    dist = [-1] * graph.order

    queue.append(anchor)
    visited[anchor] = True
    dist[anchor] = 0

    while len(queue) > 0:
        current = queue.popleft()
        if graph.adj[current] is not None:
            i = graph.adj[current].dest
            if not visited[i]:
                queue.append(i)
                visited[i] = True
                dist[i] = dist[current] + 1

    return dist


# DFS
def dfs(graph: Graph | SuccessorGraph, anchor = 0) -> Sequence[bool]:
    """run the depth-first search algorithm on a graph

    returns an array indicating whether each node can be reached from the anchor."""

    if graph.order == 0:
        raise IndexError("cannot run dfs on empty graph")
    if not 0 <= anchor < graph.order:
        raise IndexError("vertex does not exist in graph")

    visited = [False] * graph.order

    if isinstance(graph, ListGraph):
        _dfs_list(graph, anchor, visited)
        return visited
    elif isinstance(graph, MatrixGraph):
        _dfs_matrix(graph, anchor, visited)
        return visited
    elif isinstance(graph, SuccessorGraph):
        _dfs_successor(graph, anchor, visited)
        return visited

    raise NotImplementedError(f"dfs not supported for '{type(graph).__name__}'")


def _dfs_list(graph: ListGraph, current: int, visited: list[bool]) -> None:
    """dfs helper function for list graphs"""

    visited[current] = True

    for e in graph.adj[current]:
        if not visited[e.dest]:
            _dfs_list(graph, e.dest, visited)


def _dfs_matrix(graph: MatrixGraph, current: int, visited: list[bool]) -> None:
    """dfs helper function for list graphs"""

    visited[current] = True

    for i, e in enumerate(graph.adj[current]):
        if e != graph.default_value and not visited[i]:
            _dfs_matrix(graph, i, visited)


def _dfs_successor(graph: SuccessorGraph, current: int, visited: list[bool]) -> None:
    """dfs helper function for successor graphs"""

    visited[current] = True

    if graph.adj[current] is not None:
        i = graph.adj[current].dest
        if not visited[i]:
            _dfs_successor(graph, i, visited)