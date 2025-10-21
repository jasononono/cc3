from .graph import *
from .traversal import *
from .cycle import *
from .graphics import *


graph_variants = {"list": ListGraph,
                  "matrix": MatrixGraph}
                  
def new(variant = "list", *args, **kwargs):
    if variant in graph_variants:
        return graph_variants[variant](*args, **kwargs)
    
    raise TypeError(f"no graph variant named '{variant}'")