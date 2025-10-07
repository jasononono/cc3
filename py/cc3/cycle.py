from .graph import ListGraph, MatrixGraph


# CYCLE DETECTION
def find_cycle(graph: ListGraph|MatrixGraph):
    return (find_cycle_directed if graph.directed else find_cycle_undirected)(graph)

# UNDIRECTED GRAPH
def find_cycle_undirected(graph: ListGraph|MatrixGraph):
    visited = [False] * graph.order
    function = _find_cycle_list_undirected if isinstance(graph, ListGraph) else _find_cycle_matrix_undirected

    for i in range(len(visited)):
        if not visited[i] and function(graph, i, -1, visited):
            return True
    return False

def _find_cycle_list_undirected(graph, current, parent, visited):
    visited[current] = True
    for e in graph.list[current]:
        if e.dest == parent:
            continue
        if visited[e.dest] or _find_cycle_list_undirected(graph, e.dest, current, visited):
            return True
    return False

def _find_cycle_matrix_undirected(graph, current, parent, visited):
    visited[current] = True
    for i in range(graph.order):
        if not graph.matrix[current][i] or i == parent:
            continue
        if visited[i] or _find_cycle_matrix_undirected(graph, i, current, visited):
            return True
    return False

# DIRECTED GRAPH
def find_cycle_directed(graph: ListGraph|MatrixGraph):
    visited = [0] * graph.order
    function = _find_cycle_list_directed if isinstance(graph, ListGraph) else _find_cycle_matrix_directed

    for i in range(len(visited)):
        if not visited[i] and function(graph, i, visited):
            return True
    return False

def _find_cycle_list_directed(graph, current, visited):
    visited[current] = 1
    for e in graph.list[current]:
        if visited[e.dest] == 1 or (not visited[e.dest] and _find_cycle_list_directed(graph, e.dest, visited)):
            return True

    visited[current] = 2
    return False

def _find_cycle_matrix_directed(graph, current, visited):
    visited[current] = 1
    for i in range(graph.order):
        if not graph.matrix[current][i]:
            continue
        if visited[i] == 1 or (not visited[i] and _find_cycle_matrix_directed(graph, i, visited)):
            return True

    visited[current] = 2
    return False
