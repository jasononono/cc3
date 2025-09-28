from collections import deque


# BFS
def bfs(graph, anchor = 0):
    queue = deque()
    visited = [False] * graph.order
    dist = [-1] * graph.order

    queue.append(anchor)
    visited[anchor] = True
    dist[anchor] = 0

    while len(queue) > 0:
        current = queue.pop()
        for e in graph.list[current]:
            if not visited[e.dest]:
                queue.append(e.dest)
                visited[e.dest] = True
                dist[e.dest] = dist[current] + 1

    return dist

# DFS
def dfs(graph, anchor = 0):
    visited = [False] * graph.order
    _dfs(graph, anchor, visited)
    return visited

def _dfs(graph, current, visited):
    visited[current] = True
    for e in graph.list[current]:
        if not visited[e.dest]:
            _dfs(graph, e.dest, visited)