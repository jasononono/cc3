from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph
from .cycle import has_cycle
from .algorithms import count_islands


def is_tree(graph: Graph | SuccessorGraph) -> bool:
    """returns a bool indicating whether a graph is a tree

    for directed graphs, this function utilizes the definition of a connected DAG where each vertex (except for root) has
    an in-degree of 1."""

    if isinstance(graph, Graph) and not graph.directed:
        if count_islands(graph) > 1:
            return False
        return not has_cycle(graph)

    in_degrees = graph.get_in_degrees()
    zero_count = 0
    for i in in_degrees:
        if i == 0:
            zero_count += 1
        if zero_count > 1 or i > 1:
            return False
    return True

def is_forest(graph: Graph | SuccessorGraph) -> bool:
    """returns a bool indicating whether a graph is a forest, a.k.a. every component is a tree

    for directed graphs, this function utilizes the definition of a connected DAG where each vertex has
    an in-degree of at most 1 (and at least one root of in-degree 0)."""

    if isinstance(graph, Graph) and not graph.directed:
        return not has_cycle(graph)

    in_degrees = graph.get_in_degrees()
    root_exists = False
    for i in in_degrees:
        if i == 0:
            root_exists = True
        elif i > 1:
            return False
    return root_exists