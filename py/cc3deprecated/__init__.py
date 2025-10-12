from .graph import *
from .traverse import *
from.cycle import *


graph_variants = {"list": Graph,
                  "matrix": MatrixGraph,
                  "functional": SuccessorGraph}

def graph(variant = "list", *args, **kwargs):
    if variant in graph_variants:
        return graph_variants[variant](*args, **kwargs)
    else:
        raise TypeError(f"No graph variant named '{variant}'")