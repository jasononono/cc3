from .graph import *
from .algorithms import *
from .traversal import *
from .cycle import *
from .topo import *
from .labeling import *
from .flags import *
from .tree import *
from .graphics import display


graph_variants = {"list": ListGraph,
                  "tree": Tree,
                  "matrix": MatrixGraph,
                  "successor": SuccessorGraph}

def new(variant = "list", *args, **kwargs) -> Graph:
    if variant in graph_variants:
        return graph_variants[variant](*args, **kwargs)

    raise TypeError(f"no graph variant named '{variant}'")
