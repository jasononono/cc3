from typing import Any, Sequence
from collections import deque
from .graph import Graph, Edge, ListGraph, MatrixGraph


class Bfs:
    """customizable bfs template.
    To override handles, create a child class of this instance."""

    def __init__(self) -> None:
        self.graph = None
        self.anchor = None

        self.queue = None
        self.visited = None
        self.current = None

    # HANDLES
    def on_start(self, graph: Graph) -> None:
        """handle called before bfs starts"""
        return

    def is_run(self, graph: Graph) -> bool:
        """if returns false, bfs halts. Checked before every pop from queue"""
        return len(self.queue) > 0

    def on_visit(self, graph: Graph):
        """called after current is popped from queue"""
        return

    def get_next(self, graph: Graph) -> Sequence[Edge]:
        """returns all edges that need to be checked"""
        return graph.get_outgoing(self.current)

    def is_visit(self, graph: Graph, e: Edge) -> bool:
        """if returns true, the destination will be pushed to the queue"""
        return not self.visited[e.dest]

    def will_visit(self, graph: Graph, e: Edge) -> None:
        """called when an edge is pushed to queue"""
        return

    def on_end(self, graph: Graph) -> Any:
        """the return value will be the result of execution"""
        return

    # END OF HANDLES

    def run(self, graph: Graph, anchor = 0) -> Any:
        """run bfs traversal on graph, with specified anchor point (depth 0)"""

        self.graph = graph
        self.anchor = anchor

        if isinstance(graph, ListGraph):
            return self._list(graph, anchor)
        if isinstance(graph, MatrixGraph):
            return self._matrix(graph, anchor)
        raise TypeError(f"'{type(graph).__name__}' is not supported")

    def _list(self, graph: ListGraph, anchor = 0):
        """run bfs traversal on ListGraph"""

        self.queue = deque()
        self.visited = [False] * graph.order

        self.queue.append(anchor)
        self.visited[anchor] = True

        self.on_start(graph)

        while self.is_run(graph):
            self.current = self.queue.popleft()
            self.on_visit(graph)

            for e in self.get_next(graph):
                if self.is_visit(graph, e):
                    self.queue.append(e.dest)
                    self.visited[e.dest] = True
                    self.will_visit(graph, e)

        return self.on_end(graph)

    def _matrix(self, graph: MatrixGraph, anchor = 0):
        raise NotImplementedError()