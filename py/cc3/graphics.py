import tkinter as tk
import numpy as np
import math, random

from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph

# CONSTANTS
screen_width = 400
screen_height = 300
target_fps = 60

node_radius = 10
outline_thickness = 2
edge_thickness = 2

colour_background = "#ffffff"
colour_foreground = "#ffffff"
colour_vertex = "#474747"
colour_vertex_outline = "#616161"
colour_vertex_highlight = "#4978cc"
colour_edge = "#364a69"

escape_force = 0.01
repulsion = 2000
spring_length = 100
spring_stiffness = 0.03
damping = 0.6
center_gravity = 0.01


def get_edges(graph: Graph | SuccessorGraph) -> np.ndarray:
    """helper function that turns the edge data of a graph into a numpy array"""

    edges = []

    if isinstance(graph, ListGraph):
        for n in graph.adj:
            for e in n:
                if not graph.directed and (e.dest, e.origin) in edges:
                    continue
                edges.append((e.origin, e.dest))

    elif isinstance(graph, MatrixGraph):
        for i, n in enumerate(graph.adj):
            for j, e in enumerate(n):
                if e != graph.default_value:
                    if not graph.directed and (j, i) in edges:
                        continue
                    edges.append((i, j))

    elif isinstance(graph, SuccessorGraph):
        for e in graph.adj:
            if e is not None:
                edges.append((e.origin, e.dest))

    return np.array(edges, dtype = np.int64)


def display(graph: Graph | SuccessorGraph) -> None:
    """create an interactive visualization of the provided graph in tkinter"""

    # tkinter initialization
    root = tk.Tk()
    canvas = tk.Canvas(root, width = screen_width, height = screen_height, bg = colour_background)
    canvas.pack()

    # initialize data
    edges = get_edges(graph)

    position = np.array(
        [[random.randint(10, screen_width - 10), random.randint(10, screen_height - 10)] for _ in range(graph.order)])
    velocity = np.zeros((graph.order, 2))

    selected_vertex = None

    # create canvas objects
    vertices = []
    labels = []
    lines = []

    arrow = tk.LAST if isinstance(graph, SuccessorGraph) or graph.directed else None
    for i in range(graph.size):
        lines.append(canvas.create_line(0, 0, 0, 0, fill = colour_edge, width = edge_thickness, arrow = arrow))

    for i in range(graph.order):
        vertices.append(canvas.create_oval(0, 0, 0, 0, fill = colour_vertex, outline = colour_vertex_outline,
                                           width = outline_thickness))
        labels.append(canvas.create_text(0, 0, text = str(i), font = ("Arial", node_radius * 4 // 5, "bold"),
                                         fill = colour_foreground))

    # UPDATE
    def vertex_repulsion(movement: np.ndarray) -> None:
        """force each vertex apart"""

        displacement = position[:, np.newaxis, :] - position[np.newaxis, :, :]
        dsq = np.sum(displacement ** 2, axis = 2, dtype = np.float64)
        np.fill_diagonal(dsq, np.inf)
        distance = np.maximum(np.sqrt(dsq), escape_force)
        dsq = np.maximum(dsq, escape_force)

        magnitude = repulsion / dsq
        unit_force = displacement / distance[:, :, np.newaxis]
        force = magnitude[:, :, np.newaxis] * unit_force
        net_force = np.sum(force, axis = 1)

        movement += net_force

    def edge_tension(movement: np.ndarray) -> None:
        """edges act as springs, holding the vertices in place"""

        displacement = position[edges[:, 1]] - position[edges[:, 0]]

        distance = np.linalg.norm(displacement, axis = 1)
        distance = np.maximum(distance, escape_force)

        magnitude = spring_stiffness * (distance - spring_length)

        unit_force = displacement / distance[:, np.newaxis]
        force = magnitude[:, np.newaxis] * unit_force
        np.add.at(movement, edges[:, 0], force)
        np.add.at(movement, edges[:, 1], -force)

    def central_gravity(movement: np.ndarray) -> None:
        """gravity that holds vertices to the center of the frame"""

        center = np.array([screen_width / 2, screen_height / 2])
        displacement = center - position
        movement += displacement * center_gravity

    def update() -> None:
        """apply physics calculations each frame

        received partial physics help from ChatGPT"""

        nonlocal position, velocity

        movement = np.zeros((graph.order, 2))
        vertex_repulsion(movement)
        edge_tension(movement)
        central_gravity(movement)

        # update position and velocity
        excluded_vel = None
        excluded_pos = None
        if selected_vertex is not None:
            excluded_vel = velocity[selected_vertex]
            excluded_pos = position[selected_vertex]

        velocity = (velocity + movement) * damping
        position = position.astype(np.float64)
        position += velocity

        if selected_vertex is not None:
            velocity[selected_vertex] = excluded_vel
            position[selected_vertex] = excluded_pos

        position[:, 0] = np.clip(position[:, 0], node_radius, screen_width - node_radius)
        position[:, 1] = np.clip(position[:, 1], node_radius, screen_height - node_radius)

        line_pos = position[edges]
        distance = line_pos[:, 1] - line_pos[:, 0]
        ratio = node_radius / np.maximum(np.linalg.norm(distance, axis = 1)[:, None], escape_force)
        offset = distance * ratio
        line_pos[:, 0] += offset
        line_pos[:, 1] -= offset

        # update graph
        for i, ((x1, y1), (x2, y2)) in enumerate(line_pos):
            canvas.coords(lines[i], x1, y1, x2, y2)

        for i, (x, y) in enumerate(position):
            canvas.coords(vertices[i], x - node_radius, y - node_radius, x + node_radius, y + node_radius)
            canvas.coords(labels[i], x, y)

        root.after(1000 // target_fps, update)

    # MOUSE ACTIONS
    def select_vertex(event) -> None:
        """select a vertex upon mouse down"""

        nonlocal selected_vertex

        minimum_dist = float('inf')
        minimum_index = None

        for i, (x, y) in enumerate(position):
            dist = math.sqrt((event.x - x) ** 2 + (event.y - y) ** 2)
            if dist <= node_radius and dist < minimum_dist:
                minimum_dist = dist
                minimum_index = i

        selected_vertex = minimum_index
        if selected_vertex is not None:
            canvas.itemconfig(vertices[selected_vertex], outline = colour_vertex_highlight)

    def deselect_vertex(event) -> None:
        """deselect a vertex upon mouse up"""

        nonlocal selected_vertex

        if selected_vertex is not None:
            canvas.itemconfig(vertices[selected_vertex], outline = colour_vertex_outline)
        selected_vertex = None

    def drag_vertex(event) -> None:
        """set the position of a vertex on drag"""

        if selected_vertex is not None:
            position[selected_vertex][0] = event.x
            position[selected_vertex][1] = event.y

    canvas.bind("<ButtonPress-1>", select_vertex)
    canvas.bind("<ButtonRelease-1>", deselect_vertex)
    canvas.bind("<B1-Motion>", drag_vertex)

    # MAINLOOP
    update()
    tk.mainloop()