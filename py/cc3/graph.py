class Edge:
    def __init__(self, dest, weight, weighted):
        self.dest = dest
        self.weight = weight
        self.weighted = weighted

    def __eq__(self, other):
        if isinstance(other, int):
            return self.dest == other
        return self.dest == other.dest and self.weight == other.weight

    def __str__(self):
        return f"[{self.dest} {self.weight}]" if self.weighted else f"[{self.dest}]"


class ListGraph:
    def __init__(self, v = 0, weighted = False, directed = False):
        self.order = v # n
        self.size = 0 # e

        self.weighted = weighted
        self.directed = directed

        self.list = [[] for _ in range(v)]

    def __str__(self):
        result = ""
        for i, n in enumerate(self.list):
            result += str(i) + " | "
            for e in n:
                result += str(e) + ' '
            result += '\n'
        return result

    # ADD VERTICES
    def add_vertices(self, amount = 1):
        self.order += amount
        self.list.extend([[] for _ in range(amount)])

    # IS EDGE
    def is_edge(self, a: int, b: int): # O(degree of a)
        if a >= self.order or b >= self.order:
            return False

        for e in self.list[a]:
            if e == b:
                return True
        return False

    # ADD EDGE
    def add_edge(self, a: int, b: int, w = 1):
        if self.is_edge(a, b):
            return False

        if a >= self.order or b >= self.order:
            self.add_vertices(max(a, b) - self.order + 1)
        if not self.weighted:
            w = 1

        self.list[a].append(Edge(b, w, self.weighted))
        if not self.directed:
            self.list[b].append(Edge(a, w, self.weighted))

        self.size += 1
        return True

    # REMOVE EDGE
    def remove_edge(self, a: int, b: int):
        result = self._remove_edge(a, b)
        if not self.directed:
            self._remove_edge(b, a)

        self.size -= 1
        return result

    def _remove_edge(self, a, b):
        for i, e in enumerate(self.list[a]):
            if e == b:
                del self.list[a][i]
                return True
        return False

    # OUT DEGREE
    def out_degree(self, v: int): # O(1)
        if v >= self.order:
            return -1
        return len(self.list[v])

    # IN DEGREE
    def in_degree(self, v: int): # O(e)
        if v >= self.order:
            return -1

        count = 0
        for i in self.list:
            for e in i:
                if e == v:
                    count += 1
        return count

    # DEGREE
    def degree(self, v: int):
        if v >= self.order:
            return -1
        return (self.in_degree(v) if self.directed else 0) + self.out_degree(v)


class MatrixGraph:
    def __init__(self, v = 0, weighted = False, directed = False):
        self.order = v  # n
        self.size = 0  # e

        self.weighted = weighted
        self.directed = directed

        self.matrix = [[0] * v for _ in range(v)]

    # ADD VERTICES
    def add_vertices(self, amount = 1):
        self.order += amount

        for i in self.matrix:
            i.extend([0] * amount)
        self.matrix.extend([[0] * self.order for _ in range(amount)])

    # IS EDGE
    def is_edge(self, a: int, b: int): # O(1)
        if a >= self.order or b >= self.order:
            return False
        return self.matrix[a][b] != 0

    # ADD EDGE
    def add_edge(self, a: int, b: int, w = 1):
        if self.is_edge(a, b):
            return False

        if a >= self.order or b >= self.order:
            self.add_vertices(max(a, b) - self.order + 1)
        if not self.weighted:
            w = 1

        self.matrix[a][b] = w
        if not self.directed:
            self.matrix[b][a] = w

        self.size += 1
        return True

    # REMOVE EDGE
    def remove_edge(self, a: int, b: int):
        if self.matrix[a][b] == 0:
            return False

        self.matrix[a][b] = 0
        if not self.directed:
            self.matrix[b][a] = 0

        self.size -= 1
        return True

    # OUT DEGREE
    def out_degree(self, v: int):  # O(n)
        if v >= self.order:
            return -1

        count = 0
        for i in self.matrix[v]:
            if i:
                count += 1
        return count

    # IN DEGREE
    def in_degree(self, v: int):  # O(n)
        if v >= self.order:
            return -1

        count = 0
        for i in range(self.order):
            if self.matrix[i][v]:
                count += 1
        return count

    # DEGREE
    def degree(self, v: int):
        if v >= self.order:
            return -1
        return (self.in_degree(v) if self.directed else 0) + self.out_degree(v)