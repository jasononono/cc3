from src import cc3


graph = cc3.new("matrix")

graph.add_edge(0, 2)
graph.add_edge(1, 3)
graph.add_edge(4, 3)
graph.add_edge(3, 5)

print(cc3.is_forest(graph))
cc3.display(graph)