# from .graph import ListGraph, MatrixGraph


# # CYCLE DETECTION
# def has_cycle(graph: Graph) -> bool:
#     if graph.directed:
#         return find_cycle_directed(graph)
#     return find_cycle_undirected(graph)
    
# # UNDIRECTED
# def find_cycle_undirected(graph: Graph) -> bool:
#     visited = [False] * graph.order
#     function = find_cycle_undirected_list if isinstance(graph, ListGraph) else find_cycle_undirected_matrix
    
#     for i in range(len(visited)):
#         if not visited[i] and function(graph, i, -1, visited):
#             return True
#     return False
    
# def find_cycle_undirected_list(graph: Graph, current: int, parent: int, visited: Sequence[bool]) -> bool: