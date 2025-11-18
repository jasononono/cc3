from .graph import *
from .traversal import *
from .cycle import *
from .topo import *
from .graphics import display


graph_variants = {"list": ListGraph,
                  "matrix": MatrixGraph,
                  "successor": SuccessorGraph}

def new(variant = "list", *args, **kwargs) -> Graph | SuccessorGraph:
    if variant in graph_variants:
        return graph_variants[variant](*args, **kwargs)

    raise TypeError(f"no graph variant named '{variant}'")


''' TODOS

tortoise and hare
tree functions on graphs (is_tree, is_forest, etc.)

tree class with:
    set_root, get_centers, get_diameter, get_radius, get_leaves
    is_ancestor, is_child, is_parent, is_descendant
    get_ancestors, get_children, get_parents, get_descendants

toposort/ toposort_all functions
    toposort_all should return a set of all unique topo-sorts of a graph
    
dependency function of Graph (does a node come before another node in the topo sort)

count_islands / count_forests function
graph to graph conversion / comparison function (change variant, from raw data, etc.)
reverse all edges in directed graph
behaviour with default operators (+, -, edge in graph, is, ==, etc.)

the traversal boilerplate thingy oh no (final boss)

'''