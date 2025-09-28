from .graph import *
from .traverse import *


graph_types = ("list", "matrix")

def graph(v = 0, weighted = False, directed = False, variant = "list"):
    if variant == "list":
        return ListGraph(v, weighted, directed)
    elif variant == "matrix":
        return MatrixGraph(v, weighted, directed)
    else:
        raise TypeError(f"No graph variant named '{variant}'")