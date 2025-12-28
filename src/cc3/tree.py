from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph
from .cycle import has_cycle


def is_tree(graph: Graph | SuccessorGraph) -> bool:
    """returns a bool indicating whether a graph is a tree

    for directed graphs, this function uses the definition of a connected DAG where each vertex (except for root) has
    an in-degree of 1."""

    return False
    #IMPLEMENTATION

def is_forest(graph: Graph | SuccessorGraph) -> bool:
    """returns a bool indicating whether a graph is a forest

    (a.k.a. every component is a tree)"""

    return False
    # cyclic = has_cycle(graph)
    # if isinstance(graph, SuccessorGraph) or graph.directed:
    #     return False
    # return cyclic
    # IMPLEMENTATION