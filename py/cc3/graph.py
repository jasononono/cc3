from __future__ import annotations
from collections.abc import Sequence
from typing import Any, Optional


class Graph:
    """a base class for graphs (does nothing)

    used to unify ListGraph and MatrixGraph"""

    def __init__(self: Graph) -> None:
        self.order = 0  # number of vertices (n)
        self.size = 0  # number of edges (e)
        self.weighted = False
        self.directed = False
        self.adj = []

    def get_data(self) -> Sequence[Sequence[Edge | int]]:
        """returns the graph's raw adjacency data"""
        raise NotImplementedError()

    # VERTEX ACCESS
    def get_outgoing(self, v: int) -> Sequence[Edge | int]:
        """returns all outgoing edges of a vertex"""
        raise NotImplementedError()

    def get_incoming(self, v: int) -> Sequence[Edge | int]:
        """returns all incoming edges of a vertex"""
        raise NotImplementedError()

    def out_degree(self, v: int) -> int:
        """returns the number of outgoing edges of a vertex"""
        raise NotImplementedError()

    def in_degree(self, v: int) -> int:
        """returns the number of incoming edges of a vertex"""
        raise NotImplementedError()

    def degree(self, v: int) -> int:
        """returns the degree of a vertex"""
        raise NotImplementedError()

    # VERTEX CONTROL
    def add_vertex(self, amount = 1) -> None:
        """push vertices to the end of the graph (newest indices)"""
        raise NotImplementedError()

    def remove_vertex(self, index: int | Sequence[int]) -> None:
        """remove vertices from graph.

        WARNING: this will shift the vertex indices"""
        raise NotImplementedError()

    def reset(self) -> None:
        """remove all edges and vertices in the graph"""
        raise NotImplementedError()

    # EDGE ACCESS
    def is_edge(self, a: int, b: int) -> bool:
        """returns a boolean indicating whether there is an edge between (a) and (b)"""
        raise NotImplementedError()

    def get_edge(self, a: int, b: int) -> Edge:
        """returns the object representing the edge between (a) and (b)"""
        raise NotImplementedError()

    def get_weight(self, a: int, b: int) -> Any:
        """returns the weight of an edge between (a) and (b)"""
        raise NotImplementedError()

    # EDGE CONTROL
    def add_edge(self, a: int, b: int, w: Any = 1, auto_expand = True) -> None:
        """insert an edge between (a) and (b).

        if vertex does not exist and auto_expand is True, the graph will automatically add vertices.

        NOTE: multiple edges between the same endpoints are not supported"""
        raise NotImplementedError()

    def remove_edge(self, a: int, b: int) -> None:
        """attempts to remove an edge between (a) and (b)"""
        raise NotImplementedError()

    def move_edge(self, a1: int, b1: int, a2: int, b2: int) -> None:
        """attempts to move an edge between (a1) and (b1) to between (a2) and (b2)"""
        raise NotImplementedError()

    def set_weight(self, a: int, b: int, w: int = 1) -> None:
        """set the weight of the edge between (a) and (b)"""
        raise NotImplementedError()

    def clear(self) -> None:
        """clears all edges in the graph"""
        raise NotImplementedError()


class Edge:
    """an edge class used in the ListGraph to store both weighted and unweighted instances"""

    def __init__(self, a: int, b: int, w: Any = 1, parent: Optional[ListGraph | SuccessorGraph] = None) -> None:
        self.origin = a
        self.dest = b
        self.weight = w
        self.parent = parent

    def __eq__(self, other: Edge) -> bool:
        return self.origin == other.origin and self.dest == other.dest

    def __str__(self) -> str:
        if isinstance(self.parent, (ListGraph, SuccessorGraph)):
            return f"[{self.dest}-{self.weight}]" if self.parent.weighted else f"[{self.dest}]"
        return f"[{self.origin}->{self.dest}-{self.weight}]"


class ListGraph(Graph):
    """a graph object variant that stores edges with an adjacency list

    NOTE: ListGraph is the most supported out of all Graph variants"""

    def __init__(self, v = 0, weighted = False, directed = False) -> None:
        super().__init__()
        if v < 0:
            raise ValueError("amount of vertices must not be negative")

        self.order = v
        self.size = 0

        self.weighted = weighted
        self.directed = directed

        self.adj = [[] for _ in range(v)]

    def __str__(self) -> str:
        result = ""
        for i, n in enumerate(self.adj):
            result += str(i) + " | "
            for e in n:
                result += str(e) + ' '
            result += '\n'
        return result.strip()

    def get_data(self) -> Sequence[Sequence[Edge]]:
        return self.adj

    # VERTEX ACCESS
    def get_outgoing(self, v: int) -> Sequence[Edge]:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return self.adj[v]

    def get_incoming(self, v: int) -> Sequence[Edge]:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        result = []
        for n in self.adj:
            for e in n:
                if e.dest == v:
                    result.append(e)
        return result

    def out_degree(self, v: int) -> int:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return len(self.adj[v])

    def in_degree(self, v: int) -> int:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        count = 0
        for n in self.adj:
            for e in n:
                if e.dest == v:
                    count += 1
        return count

    def degree(self, v: int) -> int:
        return int(self.directed) * self.in_degree(v) + self.out_degree(v)

    # VERTEX CONTROL
    def add_vertex(self, amount = 1) -> None:
        if amount < 0:
            raise ValueError("amount must not be negative")

        self.order += amount
        self.adj.extend([[] for _ in range(amount)])

    # TODO remove_vertex

    def reset(self) -> None:
        self.order = 0
        self.size = 0
        self.adj = []

    # EDGE ACCESS
    def is_edge(self, a: int, b: int) -> bool:
        if not (0 <= a < self.order and 0 <= b < self.order):
            return False

        for e in self.adj[a]:
            if e.dest == b:
                return True
        return False

    def get_edge(self, a: int, b: int) -> Edge:
        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")

        for e in self.adj[a]:
            if e.dest == b:
                return e
        raise IndexError(f"edge [{a}->{b}] not in graph")

    def get_weight(self, a: int, b: int) -> Any:
        return self.get_edge(a, b).weight

    # EDGE CONTROL
    def add_edge(self, a: int, b: int, w: Any = 1, auto_expand = True) -> None:
        if self.is_edge(a, b):
            self.set_weight(a, b, w)
            if not self.directed:
                self.set_weight(b, a, w)
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

        self.adj[a].append(Edge(a, b, w, self))
        if not self.directed:
            self.adj[b].append(Edge(b, a, w, self))
        self.size += 1

    def remove_edge(self, a: int, b: int) -> None:
        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")

        self._remove_edge(a, b)
        if not self.directed:
            self._remove_edge(b, a)
        self.size -= 1

    def _remove_edge(self, a: int, b: int) -> None:
        """helper function for remove_edge"""

        for i, e in enumerate(self.adj[a]):
            if e.dest == b:
                del self.adj[a][i]
                return
        raise IndexError(f"edge [{a}->{b}] not in graph")

    # TODO move_edge

    def set_weight(self, a: int, b: int, w: Any = 1) -> None:
        self.get_edge(a, b).weight = w

    def clear(self) -> None:
        self.size = 0
        self.adj = [[] for _ in range(self.order)]


class MatrixGraph(Graph):
    """a graph object variant that stores edges with an adjacency matrix

    the default_value parameter is used to represent the lack of an edge between two vertices
    (e.g. there are no edges between (a) and (b) if get_weight(a, b) == default_value)

    NOTE: default_value must be immutable"""

    def __init__(self, v = 0, weighted = False, directed = False, default_value: Any = None) -> None:
        super().__init__()
        if v < 0:
            raise ValueError("amount of vertices must not be negative")

        self.order = v
        self.size = 0

        self.weighted = weighted
        self.directed = directed
        self.default_value = default_value

        self.adj = [[default_value] * v for _ in range(v)]

    def __str__(self) -> str:
        result = ""
        for i, n in enumerate(self.adj):
            result += str(i) + " | "
            for e in n:
                result += str(e) + ' '
            result += '\n'
        return result.strip()

    def get_data(self) -> Sequence[Sequence[int]]:
        return self.adj

    # VERTEX ACCESS
    def get_outgoing(self, v: int) -> Sequence[int]:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return [i for i, e in enumerate(self.adj[v]) if e != self.default_value]

    def get_incoming(self, v: int) -> Sequence[int]:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return [i for i, n in enumerate(self.adj) if n[v] != self.default_value]

    def out_degree(self, v: int) -> int:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        count = 0
        for e in self.adj[v]:
            if e != self.default_value:
                count += 1
        return count

    def in_degree(self, v: int) -> int:
        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        count = 0
        for n in self.adj:
            if n[v] != self.default_value:
                count += 1
        return count

    def degree(self, v: int) -> int:
        return int(self.directed) * self.in_degree(v) + self.out_degree(v)

    # VERTEX CONTROL
    def add_vertex(self, amount = 1) -> None:
        if amount < 0:
            raise ValueError("amount must not be negative")

        self.order += amount
        for n in self.adj:
            n.extend([self.default_value] * amount)
        self.adj.extend([[self.default_value] * self.order for _ in range(amount)])

    # TODO remove_vertex

    def reset(self) -> None:
        self.order = 0
        self.size = 0
        self.adj = []

    # EDGE ACCESS
    def is_edge(self, a: int, b: int) -> bool:
        if not (0 <= a < self.order and 0 <= b < self.order):
            return False

        return self.adj[a][b] != self.default_value

    def get_edge(self, a: int, b: int) -> Any:
        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")

        if self.adj[a][b] == self.default_value:
            raise IndexError(f"edge [{a}->{b}] not in graph")
        return self.adj[a][b]

    def get_weight(self, a: int, b: int) -> Any:
        return self.adj[a][b]

    # EDGE CONTROL
    def add_edge(self, a: int, b: int, w: Any = 1, auto_expand = True) -> None:
        if self.is_edge(a, b):
            self.set_weight(a, b, w)
            if not self.directed:
                self.set_weight(b, a, w)
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

        self.adj[a][b] = w
        if not self.directed:
            self.adj[b][a] = w
        self.size += 1

    def remove_edge(self, a: int, b: int) -> None:
        if not 0 <= a < self.order:
            raise IndexError(f"vertex ({a}) does not exist in graph")
        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")

        self.adj[a][b] = self.default_value
        if not self.directed:
            self.adj[b][a] = self.default_value
        self.size -= 1

    # TODO move_edge

    def set_weight(self, a: int, b: int, w: Any = 1) -> None:
        self.adj[a][b] = w

    def clear(self) -> None:
        self.size = 0
        self.adj = [[self.default_value] * self.order for _ in range(self.order)]


class SuccessorGraph:
    """a graph variant that has at most one outgoing edge per vertex"""

    def __init__(self, v = 0, weighted = False) -> None:
        if v < 0:
            raise ValueError("amount of vertices must not be negative")

        self.order = v
        self.size = 0

        self.weighted = weighted

        self.adj: list[Edge | None] = [None] * v

    def __str__(self) -> str:
        return ' '.join([str(i) for i in self.adj])

    def get_data(self) -> Sequence[Edge | None]:
        """returns the graph's raw adjacency data"""

        return self.adj

    # VERTEX ACCESS
    def get_outgoing(self, v: int) -> Edge:
        """returns the outgoing edge of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")
        if self.adj[v] is None:
            raise ValueError(f"no edge starts on vertex ({v})")

        return self.adj[v]

    def get_incoming(self, v: int) -> Sequence[Edge]:
        """returns all outgoing edges of a vertex"""

        if not 0 <= v < self.order:
            raise IndexError(f"vertex ({v}) does not exist in graph")

        return [e for e in self.adj if e is not None and e.dest == v]

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

    def is_functional(self) -> bool:
        """returns whether every vertex has an outgoing edge"""

        return not bool(len([False for e in self.adj if e is None]))

    # VERTEX CONTROL
    def add_vertex(self, amount = 1) -> None:
        """push vertices to the end of the graph (newest indices)"""

        if amount < 0:
            raise ValueError("amount must not be negative")

        self.order += amount
        self.adj.extend([None for _ in range(amount)])

    # TODO remove_vertex

    def reset(self) -> None:
        self.order = 0
        self.size = 0
        self.adj = []

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

        return self.adj[a]

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

        if not 0 <= b < self.order:
            raise IndexError(f"vertex ({b}) does not exist in graph")

        self.get_outgoing(a).dest = b

    def set_weight(self, a: int, b: int = None, w: Any = 1) -> None:
        """set the weight of the edge starting on (a)

        the parameter (b) is optional for checking if the requested edge exists"""

        if b is None:
            self.get_outgoing(a).weight = w
        else:
            self.get_edge(a, b).weight = w

    def clear(self) -> None:
        self.size = 0
        self.adj = [None] * self.order