from .graph import Graph, ListGraph, MatrixGraph
from .successor import SuccessorGraph
from .cycle import has_cycle


def is_tree(graph: Graph | SuccessorGraph) -> bool:
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