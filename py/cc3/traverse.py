from collections import deque
from .graph import ListGraph, MatrixGraph


# BFS
def bfs(graph: ListGraph|MatrixGraph, anchor = 0):
    return _bfs_list(graph, anchor) if isinstance(graph, ListGraph) else _bfs_matrix(graph, anchor)

def _bfs_list(graph, anchor):
    queue = deque()
    visited = [False] * graph.order
    dist = [-1] * graph.order

    queue.append(anchor)
    visited[anchor] = True
    dist[anchor] = 0

    while len(queue) > 0:
        current = queue.popleft()
        for e in graph.list[current]:
            if not visited[e.dest]:
                queue.append(e.dest)
                visited[e.dest] = True
                dist[e.dest] = dist[current] + 1

    return dist

def _bfs_matrix(graph, anchor):
    queue = deque()
    visited = [False] * graph.order
    dist = [-1] * graph.order

    queue.append(anchor)
    visited[anchor] = True
    dist[anchor] = 0

    while len(queue) > 0:
        current = queue.popleft()
        for e, w in enumerate(graph.matrix[current]):
            if w != 0 and not visited[e]:
                queue.append(e)
                visited[e] = True
                dist[e] = dist[current] + 1

    return dist

# 0-1 BFS
def zero_one_bfs(graph: ListGraph, anchor = 0):
    queue = deque()
    visited = [False] * graph.order
    dist = [-1] * graph.order

    queue.append(anchor)
    visited[anchor] = True
    dist[anchor] = 0

    while len(queue) > 0:
        current = queue.popleft()
        for e in graph.list[current]:
            if not visited[e.dest]:
                if e.weight:
                    queue.append(e.dest)
                    dist[e.dest] = dist[current] + 1
                else:
                    queue.appendleft(e.dest)
                    dist[e.dest] = dist[current]
                visited[e.dest] = True

    return dist

# DFS
def dfs(graph: ListGraph|MatrixGraph, anchor = 0):
    visited = [False] * graph.order
    _dfs_list(graph, anchor, visited) if isinstance(graph, ListGraph) else _dfs_matrix(graph, anchor, visited)
    return visited

def _dfs_list(graph, current, visited):
    visited[current] = True
    for e in graph.list[current]:
        if not visited[e.dest]:
            _dfs_list(graph, e.dest, visited)

def _dfs_matrix(graph, current, visited):
    visited[current] = True
    for e, w in enumerate(graph.matrix[current]):
        if w != 0 and not visited[e]:
            _dfs_matrix(graph, e, visited)