from .graph import Graph
from .successor import SuccessorGraph
from typing import Any


class LabelMap:
    """maps unique labels to indices of a graph"""

    def __init__(self, graph: Graph | SuccessorGraph) -> None:
        self.parent = graph
        self.map = []
        self.find = {}
        self.unique = None
        self.set_parent(graph)

    def check(self) -> bool:
        """checks whether labels are unique"""

        defaults = self.map.count("")
        return len(set(self.map)) + defaults - 1 == len(self.map)

    def update(self) -> None:
        """updates the label map"""

        self.map = self.parent.get_labels()
        self.unique = self.check()
        if self.unique:
            self.find.clear()
            for i, l in enumerate(self.map):
                self.find[l] = i

    def set_parent(self, graph: Graph | SuccessorGraph) -> None:
        """updates the label map and bind to another graph"""

        self.parent = graph
        self.update()

    def index(self, label: Any) -> int:
        """convert a label into index"""

        if not self.unique:
            raise ValueError("labels are not unique")
        if label == "":
            raise ValueError("label is empty")

        return self.find[label]

    def label(self, index: int) -> Any:
        """convert an index into label"""

        return self.parent.get_label(index)