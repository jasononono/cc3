import pyglet, numpy, random, math
from typing import Tuple

from .graph import Graph, ListGraph, MatrixGraph, SuccessorGraph


class Attributes:
    """class that stores all graphics attributes"""

    def __init__(self) -> None:
        self.window_width = 1000
        self.window_height = 750
        self.window_fps = 1 / 60
        self.window_antialias = 8

        self.colour_bg = (206, 213, 222)
        self.colour_fg = (255, 255, 255)
        self.colour_vertex = (57, 67, 82)
        self.colour_outline = (44, 52, 64)
        self.colour_outline_selected = (82, 112, 156)
        self.colour_edge = (26, 43, 69)

        self.vertex_radius = 30
        self.vertex_quality = None
        self.vertex_outline = 5

        self.edge_thickness = 5

        self.physics_escape_force = 0.01
        self.physics_repulsion = 20000
        self.physics_damping = 0.6
        self.physics_spring_stiffness = 0.05
        self.physics_spring_length = 200


_attributes = Attributes()

def reset_attributes() -> None:
    """reset all graphics attributes to their default"""
    _attributes.__init__()

def _valid_attribute(name, target_name, value, target_type) -> bool:
    """helper function of set_attribute that checks if name-value combination is valid"""

    if name == target_name:
        if isinstance(value, target_type):
            return True
        raise TypeError(f"attribute '{name}' must be {target_type}, not {type(value).__name__}")
    return False

def set_attribute(name, value) -> None:
    """set the graphics module's properties (e.g. window resolution, fps, physics constants, etc.)

    here is a list of available attributes:"""

    if _valid_attribute(name, "window_width", value, int):
        _attributes.window_width = value
    elif _valid_attribute(name, "window_height", value, int):
        _attributes.window_height = value
    elif _valid_attribute(name, "window_fps", value, int):
        _attributes.window_fps = 1 / value
    elif _valid_attribute(name, "window_antialias", value, int):
        _attributes.window_antialias = value

    elif _valid_attribute(name, "colour_bg", value, Tuple[int, int, int]):
        _attributes.colour_bg = value
    elif _valid_attribute(name, "colour_fg", value, Tuple[int, int, int]):
        _attributes.colour_fg = value
    elif _valid_attribute(name, "colour_vertex", value, Tuple[int, int, int]):
        _attributes.colour_vertex = value
    elif _valid_attribute(name, "colour_outline", value, Tuple[int, int, int]):
        _attributes.colour_outline = value
    elif _valid_attribute(name, "colour_outline_selected", value, Tuple[int, int, int]):
        _attributes.colour_outline_selected = value

    elif _valid_attribute(name, "vertex_radius", value, int):
        _attributes.vertex_radius = value
    elif _valid_attribute(name, "vertex_quality", value, int | None):
        _attributes.vertex_quality = value
    elif _valid_attribute(name, "vertex_outline", value, int):
        _attributes.vertex_outline = value

    elif _valid_attribute(name, "physics_escape_force", value, float):
        _attributes.physics_escape_force = value
    elif _valid_attribute(name, "physics_repulsion", value, float):
        _attributes.physics_repulsion = value
    elif _valid_attribute(name, "physics_damping", value, float):
        _attributes.physics_damping = value
    elif _valid_attribute(name, "physics_spring_stiffness", value, float):
        _attributes.physics_spring_stiffness = value
    elif _valid_attribute(name, "physics_spring_length", value, float):
        _attributes.physics_spring_length = value

    else:
        raise TypeError(f"attribute '{name}' does not exist")


def get_edges(graph: Graph | SuccessorGraph) -> numpy.ndarray:
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

    return numpy.array(edges, dtype = numpy.int32)

def randomize_positions(amount):
    """create a random list of vertex positions"""

    vertex_position = [(random.randint(_attributes.vertex_radius, _attributes.window_width - _attributes.vertex_radius),
                        random.randint(_attributes.vertex_radius, _attributes.window_height - _attributes.vertex_radius))
                        for _ in range(amount)]
    return numpy.array(vertex_position, dtype = numpy.float32)

def display(graph: Graph | SuccessorGraph) -> None:
    """create an interactive visualization of the provided graph"""

    config = pyglet.gl.Config(sample_buffers = 1, samples = 8, double_buffer = True)
    window = pyglet.window.Window(_attributes.window_width, _attributes.window_height, "cc3", config = config)
    pyglet.gl.glClearColor(*_attributes.colour_bg, 1)
    batch = pyglet.graphics.Batch()


    class Data:
        """object that manages the graph visualization data"""

        def __init__(self) -> None:
            self.edges = get_edges(graph)
            self.vertex_position = randomize_positions(graph.order)
            self.vertex_velocity = numpy.zeros((graph.order, 2), dtype = numpy.float32)
            self.vertex_movement = numpy.zeros((graph.order, 2), dtype = numpy.float32)

            self.selected_vertex = None

        def vertex_repulsion(self):
            """force each vertex apart"""

            displacement = self.vertex_position[:, numpy.newaxis, :] - self.vertex_position[numpy.newaxis, :, :]
            dsq = numpy.sum(displacement ** 2, axis = 2)
            numpy.fill_diagonal(dsq, numpy.inf)
            distance = numpy.maximum(numpy.sqrt(dsq), _attributes.physics_escape_force)
            dsq = numpy.maximum(dsq, _attributes.physics_escape_force)

            magnitude = _attributes.physics_repulsion / dsq
            unit_force = displacement / distance[:, :, numpy.newaxis]
            force = magnitude[:, :, numpy.newaxis] * unit_force
            net_force = numpy.sum(force, axis = 1)

            self.vertex_movement += net_force

        def edge_tension(self) -> None:
            """edges act as springs, holding the vertices in place"""

            displacement = self.vertex_position[self.edges[:, 1]] - self.vertex_position[self.edges[:, 0]]

            distance = numpy.linalg.norm(displacement, axis = 1)
            distance = numpy.maximum(distance, _attributes.physics_escape_force)

            magnitude = _attributes.physics_spring_stiffness * (distance - _attributes.physics_spring_length)

            unit_force = displacement / distance[:, numpy.newaxis]
            force = magnitude[:, numpy.newaxis] * unit_force
            numpy.add.at(self.vertex_movement, self.edges[:, 0], force)
            numpy.add.at(self.vertex_movement, self.edges[:, 1], -force)

        def central_gravity(self) -> None:
            """pulls the whole graph to the center"""

            center = numpy.sum(self.vertex_position)
            displacement = -(self.vertex_position - center)
            self.vertex_movement += displacement * 0.01

        def update(self) -> None:
            """update graph visuals"""

            self.vertex_movement.fill(0)
            self.vertex_repulsion()
            self.edge_tension()
            #self.central_gravity()

            excluded_vel = None
            excluded_pos = None
            if self.selected_vertex is not None:
                excluded_vel = self.vertex_velocity[self.selected_vertex].copy()
                excluded_pos = self.vertex_position[self.selected_vertex].copy()

            self.vertex_velocity = (self.vertex_velocity + self.vertex_movement) * _attributes.physics_damping
            self.vertex_position += self.vertex_velocity

            if self.selected_vertex is not None:
                self.vertex_velocity[self.selected_vertex] = excluded_vel
                self.vertex_position[self.selected_vertex] = excluded_pos

            self.vertex_position[:, 0] = numpy.clip(self.vertex_position[:, 0], _attributes.vertex_radius,
                                                    _attributes.window_width - _attributes.vertex_radius)
            self.vertex_position[:, 1] = numpy.clip(self.vertex_position[:, 1], _attributes.vertex_radius,
                                                    _attributes.window_height - _attributes.vertex_radius)


    data = Data()

    vertex_objects = []
    outline_objects = []
    index_objects = []
    edge_objects = []

    for n in range(graph.order):
        group = pyglet.graphics.Group(n + 1)
        outline_objects.append(pyglet.shapes.Circle(0, 0, _attributes.vertex_radius + _attributes.vertex_outline,
                                                    color = _attributes.colour_outline, batch = batch, group = group))
        vertex_objects.append(pyglet.shapes.Circle(0, 0, _attributes.vertex_radius,
                                                   color = _attributes.colour_vertex, batch = batch, group = group))

        index_objects.append(pyglet.text.Label(str(n), 0, 0, anchor_x = "center", anchor_y = "bottom",
                                               font_name = "Arial", font_size = _attributes.vertex_radius * 0.8,
                                               batch = batch, group = group))

    group = pyglet.graphics.Group(0)
    for i in range(graph.size):
        edge_objects.append(pyglet.shapes.Line(0, 0, 0, 0, _attributes.edge_thickness,
                                               _attributes.colour_edge, batch = batch, group = group))


    def refresh() -> None:
        """update position data"""

        for i in range(graph.order):
            vertex_objects[i].x, vertex_objects[i].y = data.vertex_position[i]
            outline_objects[i].x, outline_objects[i].y = data.vertex_position[i]

            index_objects[i].x = data.vertex_position[i][0]
            index_objects[i].y = data.vertex_position[i][1] - index_objects[i].content_height / 2

        edge_position = data.vertex_position[data.edges]
        distance = edge_position[:, 1] - edge_position[:, 0]
        ratio = _attributes.vertex_radius / numpy.maximum(numpy.linalg.norm(distance, axis = 1)[:, None],
                                                          _attributes.physics_escape_force)
        offset = distance * ratio
        edge_position[:, 0] += offset
        edge_position[:, 1] -= offset

        for i, (p1, p2) in enumerate(edge_position):
            edge_objects[i].x, edge_objects[i].y = p1
            edge_objects[i].x2, edge_objects[i].y2 = p2


    @window.event
    def on_mouse_press(x, y, button, modifiers) -> None:
        if button != pyglet.window.mouse.LEFT:
            return

        minimum_dist = float('inf')
        minimum_index = None

        for i, p in enumerate(data.vertex_position):
            dist = math.sqrt((p[0] - x) ** 2 + (p[1] - y) ** 2)
            if dist <= _attributes.vertex_radius and dist < minimum_dist:
                minimum_dist = dist
                minimum_index = i

        data.selected_vertex = minimum_index
        if data.selected_vertex is not None:
            outline_objects[data.selected_vertex].color = _attributes.colour_outline_selected

    @window.event
    def on_mouse_release(x, y, button, modifiers) -> None:
        if data.selected_vertex is not None:
            outline_objects[data.selected_vertex].color = _attributes.colour_outline
        data.selected_vertex = None

    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers) -> None:
        if data.selected_vertex is not None:
            data.vertex_position[data.selected_vertex] = x, y

    @window.event
    def on_draw() -> None:
        data.update()
        refresh()
        window.clear()
        batch.draw()


    pyglet.app.run(_attributes.window_fps)