class Edge:
    def __init__(self, dest, weight):
        self.dest = dest
        self.weight = weight

    def __eq__(self, other):
        if isinstance(other, int):
            return self.dest == other
        return self.dest == other.dest and self.weight == other.weight


class Graph:
    def __init__(self, v = 0, weighted = False, directed = False):
        self.order = v # n
        self.size = 0 # e

        self.weighted = weighted
        self.directed = directed

        self.matrix: list[list[int]] = [[0] * v for _ in range(v)]
        self.list: list[list[Edge]] = [[] for _ in range(v)]

    # ADD VERTICES
    def add_vertices(self, amount = 1):
        self.order += amount

        for i in self.matrix:
            i.extend([0] * amount)
        self.matrix.extend([[0] * self.order for _ in range(amount)])

        self.list.extend([[] for _ in range(amount)])

    # IS EDGE
    def is_edge(self, a, b):
        if a >= self.order or b >= self.order:
            return False
        return self.is_edge_matrix(a, b)

    def is_edge_matrix(self, a, b): # O(1)
        return self.matrix[a][b] != 0

    def is_edge_list(self, a, b): # O(degree of a)
        for e in self.list[a]:
            if e == b:
                return True
        return False

    # ADD EDGE
    def add_edge(self, a, b, w = 1):
        if self.is_edge(a, b):
            return False

        if a >= self.order or b >= self.order:
            self.add_vertices(max(a, b) - self.order + 1)

        self._add_edge(a, b, w)
        if not self.directed:
            self._add_edge(b, a, w)

        self.size += 1
        return True

    def _add_edge(self, a, b, w):
        self.matrix[a][b] = w if self.weighted else 1
        self.list[a].append(Edge(b, w if self.weighted else 1))

    # REMOVE EDGE
    def remove_edge(self, a, b):
        result = self._remove_edge(a, b)
        if not self.directed:
            self._remove_edge(b, a)

        self.size -= 1
        return result

    def _remove_edge(self, a, b):
        self.matrix[a][b] = 0
        for i, e in enumerate(self.list[a]):
            if e == b:
                del self.list[a][i]
                return True
        return False

    # OUT DEGREE
    def out_degree(self, v):
        if v >= self.order:
            return -1
        return self.out_degree_list(v)

    def out_degree_matrix(self, v): # O(n)
        count = 0
        for i in self.matrix[v]:
            if i:
                count += 1
        return count

    def out_degree_list(self, v): # O(1)
        return len(self.list[v])

    # IN DEGREE
    def in_degree(self, v):
        if v >= self.order:
            return -1
        return (self.in_degree_matrix(v) if self.order < self.size else
                self.in_degree_list(v))

    def in_degree_matrix(self, v): # O(n)
        count = 0
        for i in range(self.order):
            if self.matrix[i][v]:
                count += 1
        return count

    def in_degree_list(self, v): # O(e)
        count = 0
        for i in self.list:
            for e in i:
                if e == v:
                    count += 1
        return count

    # DEGREE
    def degree(self, v):
        if v >= self.order:
            return -1
        return (self.in_degree(v) if self.directed else 0) + self.out_degree(v)
