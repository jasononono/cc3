from __future__ import annotations
from collections.abc import Sequence
from typing import Any
from .graph import Edge


class SuccessorGraph:
    """a graph variant that has at most one outgoing edge per vertex"""

    def __init__(self, v = 0, weighted = False) -> None:
        if v < 0:
            raise ValueError("amount of vertices must not be negative")

        self.order = v
        self.size = 0

        self.weighted = weighted

        self.adj: list[Edge | None] = [None] * v
        self.labels = [""] * v

    def __str__(self) -> str:
        labels = ""
        string = ""
        for i, (n, l) in enumerate(zip(self.adj, self.labels)):
            label = str(i) + ("" if l == "" else f"({l})")
            align = max(len(label), len(str(n))) + 1
            labels += label + ' ' * (align - len(label))
            string += str(n) + ' ' * (align - len(str(n)))
        return labels + '\n' + string

    def get_data(self) -> Sequence[Edge | None]:
        """returns the graph's raw adjacency data"""

        return [e.copy() for e in self.adj]

    def get_labels(self) -> Sequence[str]:
        """returns the labels of all vertices"""

        return self.labels.copy()

    # VERTEX ACCESS
    def get_outgoing(self, v: int) -> Edge:
        """returns the outgoing edge of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")
        if self.adj[v] is None:
            raise ValueError(f"no edge starts on vertex ({v})")

        return self.adj[v].copy()

    def get_incoming(self, v: int) -> Sequence[Edge]:
        """returns all outgoing edges of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return [e.copy() for e in self.adj if e is not None and e.dest == v]

    def out_degree(self, v: int) -> int:
        """returns the number of outgoing edges of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return int(self.adj[v] is not None)

    def in_degree(self, v: int) -> int:
        """returns the number of incoming edges of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        count = 0
        for n in self.adj:
            if n is not None and n.dest == v:
                count += 1
        return count

    def degree(self, v: int) -> int:
        """returns the degree of a vertex"""

        return self.in_degree(v) + self.out_degree(v)

    def get_label(self, v: int) -> str:
        """returns the label of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return self.labels[v]

    # VERTEX CONTROL
    def add_vertex(self, amount = 1) -> None:
        """push vertices to the end of the graph (newest indices)"""

        if amount < 0:
            raise ValueError("amount must not be negative")

        self.order += amount
        self.adj.extend([None] * amount)
        self.labels.extend([""] * amount)

    # TODO remove_vertex

    def reset(self) -> None:
        self.order = 0
        self.size = 0
        self.adj = []
        self.labels = []

    def add_vertex_by_label(self, label: str) -> None:
        """push a vertex with a designated label to the end of the graph (newest index)"""

        self.order += 1
        self.adj.append(None)
        self.labels.append(label)

    def add_vertices_by_label(self, labels: Sequence[str]) -> None:
        """push vertices with designated labels to the end of the graph (newest indices)"""

        self.order += len(labels)
        self.adj.extend([None] * len(labels))
        self.labels.extend(labels)

    def set_label(self, v: int, label: str) -> None:
        """set the label of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        self.labels[v] = label

    # EDGE ACCESS
    def is_edge(self, a: int, b: int) -> bool:
        """returns a boolean indicating whether there is an edge between (a) and (b)"""

        if not (0 <= a < self.order and 0 <= b < self.order):
            return False

        return self.adj[a] is not None and self.adj[a].dest == b

    def get_edge(self, a: int, b: int) -> Edge:
        """returns the object representing the edge between (a) and (b)"""

        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")

        if self.adj[a] is None:
            raise ValueError(f"no edge starts on vertex ({a})")
        if self.adj[a].dest != b:
            raise IndexError(f"edge [{a}->{b}] not in graph")

        return self.adj[a].copy()

    def get_weight(self, a: int, b: int = None) -> Any:
        """returns the weight of an edge between (a) and (b)

        the parameter (b) is optional for checking if the requested edge exists"""

        if b is None:
            return self.get_outgoing(a).weight
        return self.get_edge(a, b).weight

    # EDGE CONTROL
    def add_edge(self, a: int, b: int, w: Any = 1, auto_expand = True) -> None:
        """insert an edge between (a) and (b).

        if vertex does not exist and auto_expand is True, the graph will automatically add vertices."""

        if self.is_edge(a, b):
            self.set_weight(a, w = w)
            return
        if a < 0 or b < 0:
            raise IndexError(f"vertices must not be negative")

        if auto_expand:
            if a >= self.order or b >= self.order:
                self.add_vertex(max(a, b) - self.order + 1)
        else:
            if not 0 <= a < self.order:
                raise IndexError(f"vertex ({a}) does not exist in graph")
            if not 0 <= b < self.order:
                raise IndexError(f"vertex ({b}) does not exist in graph")

        if self.out_degree(a):
            self.move_edge(a, b)
            self.set_weight(a, w = w)
            return

        self.adj[a] = Edge(a, b, w, self)
        self.size += 1

    def remove_edge(self, a: int, b: int) -> None:
        """attempts to remove the edge between (a) and (b)"""

        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")
        if not self.is_edge(a, b):
            raise IndexError(f"edge [{a}->{b}] not in graph")

        self.adj[a] = None
        self.size -= 1

    def move_edge(self, a: int, b: int) -> None:
        """attempts to redirect the edge starting on (a) to end at (b)"""

        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")
        if self.adj[a] is None:
            raise ValueError(f"no edge starts on vertex ({a})")

        self.adj[a].dest = b

    def set_weight(self, a: int, b: int = None, w: Any = 1) -> None:
        """set the weight of the edge starting on (a)

        the parameter (b) is optional for checking if the requested edge exists"""

        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if self.adj[a] is None:
            raise ValueError(f"no edge starts on vertex ({a})")
        if b is not None:
            if not 0 <= b < self.order:
                raise IndexError(f"vertex ({b}) does not exist in graph")
            if not self.is_edge(a, b):
                raise IndexError(f"edge [{a}->{b}] not in graph")

        self.adj[a].weight = w

    def clear(self) -> None:
        """clears all edges in the graph"""

        self.size = 0
        self.adj = [None] * self.order

    def copy(self) -> SuccessorGraph:
        """make an identical copy of the current graph"""

        graph = SuccessorGraph(self.order, self.weighted)
        graph.size = self.size

        for i, e in enumerate(self.adj):
            if e is None:
                continue
            edge = e.copy()
            edge.parent = graph
            graph.adj[i] = edge

        graph.labels = self.get_labels()

        return graph

    def __copy__(self) -> SuccessorGraph:
        return self.copy()

    def __deepcopy__(self, memo) -> SuccessorGraph:
        return self.copy()


# TORTOISE AND HARE
def cycle_start(graph: SuccessorGraph, source = 0):
    """returns the start of a cycle in a successor graph using Floyd's algorithm

    if no cycle is detected beginning at the source, -1 will be returned"""

    if graph.adj[source] is None or graph.adj[graph.adj[source].dest] is None:
        return -1

    tortoise = graph.adj[source].dest
    hare = graph.adj[graph.adj[source].dest].dest

    while tortoise != hare:
        tortoise = graph.adj[tortoise].dest
        hare = graph.adj[hare].dest
        if hare is None:
            return -1
        hare = graph.adj[hare].dest
        if hare is None:
            return -1

    tortoise = source

    while tortoise != hare:
        tortoise = graph.adj[tortoise].dest
        hare = graph.adj[hare].dest

    return hare