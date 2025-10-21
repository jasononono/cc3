import tkinter as tk
import math, random, time

from .graph import ListGraph


# CONSTANTS
screen_width = 400 # greater than 20
screen_height = 300 # greater than 20
node_radius = 10

escape_force = 0.01
repulsion = 3000
spring_length = 100
spring_stiffness = 0.03
damping = 0.8
center_gravity = 0.02


def display(graph: ListGraph) -> None:
    """create a interactive visualization of the provided graph in tkinter"""
    
    root = tk.Tk()
    canvas = tk.Canvas(root, width = screen_width, height = screen_height, bg = "white")
    canvas.pack()
    
    position = [[random.randint(10, screen_width - 10), random.randint(10, screen_height - 10)] for _ in range(graph.order)]
    velocity = [[0, 0] for _ in range(graph.order)]
    
    selected_vertex = None
    
    
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
        
        
    def deselect_vertex(event) -> None:
        """deselect a vertex upon mouse up"""
        
        nonlocal selected_vertex
        
        selected_vertex = None
        
        
    def drag_vertex(event) -> None:
        """set the position of a vertex on drag"""
        
        if selected_vertex is not None:
            position[selected_vertex][0] = event.x
            position[selected_vertex][1] = event.y
    
    
    def update() -> None:
        """apply physics calculations each frame
        
        received partial physics help from ChatGPT"""
        
        movement = [[0, 0] for _ in range(graph.order)]
       
        for i in range(graph.order - 1):
            for j in range(i + 1, graph.order):
                dx = position[i][0] - position[j][0]
                dy = position[i][1] - position[j][1]
                dsq = dx ** 2 + dy ** 2
                dist = math.sqrt(dsq) or escape_force
                
                force = repulsion / (dsq or escape_force)
                fx = force * dx / dist
                fy = force * dy / dist
                
                movement[i][0] += fx
                movement[i][1] += fy
                movement[j][0] -= fx
                movement[j][1] -= fy
                
        for n in graph.adj:
            for e in n:
                dx = position[e.dest][0] - position[e.origin][0]
                dy = position[e.dest][1] - position[e.origin][1]
                dist = math.sqrt(dx ** 2 + dy ** 2) or escape_force
                
                displacement = dist - spring_length
                force = spring_stiffness * displacement
                fx = force * dx / dist
                fy = force * dy / dist
                
                movement[e.origin][0] += fx
                movement[e.origin][1] += fy
                movement[e.dest][0] -= fx
                movement[e.dest][1] -= fy
                
        for i in range(graph.order):
            dx = screen_width / 2 - position[i][0]
            dy = screen_height / 2 - position[i][1]
            movement[i][0] += dx * center_gravity
            movement[i][1] += dy * center_gravity
                
        for i in range(graph.order):
            if i != selected_vertex:
                
                velocity[i][0] = (velocity[i][0] + movement[i][0]) * damping
                velocity[i][1] = (velocity[i][1] + movement[i][1]) * damping
    
                position[i][0] += velocity[i][0]
                position[i][1] += velocity[i][1]

            position[i][0] = min(max(node_radius, position[i][0]), screen_width - node_radius)
            position[i][1] = min(max(node_radius, position[i][1]), screen_height - node_radius)
            
        canvas.delete("all")
        for n in graph.adj:
            for e in n:
                canvas.create_line(*position[e.origin], *position[e.dest], fill = "gray", width = 2)
        for i, (x, y) in enumerate(position):
            canvas.create_oval(x - node_radius, y - node_radius, x + node_radius, y + node_radius, fill = "black")
            canvas.create_text(x, y, text = str(i), font = ("Arial", 8, "bold"), fill = "white")
            
        root.after(33, update)
    
    
    canvas.bind("<ButtonPress-1>", select_vertex)
    canvas.bind("<ButtonRelease-1>", deselect_vertex)
    canvas.bind("<B1-Motion>", drag_vertex)
    
    update()
    tk.mainloop()