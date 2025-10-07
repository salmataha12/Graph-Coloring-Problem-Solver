
import sys
import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from config import set_of_colors

def close_program():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        sys.exit()

def draw_graph(frame_del, num_nodes, color_of_nodes, edges, list1, root, time_taken=None, number_of_colors=None):
    frame_del.pack_forget()
    frame5 = tk.Frame(root, bg="#F5F5DC")
    frame5.pack()

    G = nx.Graph()
    for i in range(1, num_nodes + 1):
        G.add_node(str(i))
    G.add_edges_from(list1)

    fig = plt.figure(figsize=(5, 4), facecolor="#F5F5DC")
    plot1 = fig.add_subplot(111)
    plot1.set_facecolor("#F5F5DC")
    plot1.set_xticks([])
    plot1.set_yticks([])
    plot1.set_frame_on(False)

    colors = [set_of_colors[color_of_nodes[i]] for i in range(1, num_nodes + 1)]

    nx.draw(
        G,
        with_labels=True,
        ax=plot1,
        node_color=colors,
        edgecolors="black",
        linewidths=1,
        node_size=800,
        font_weight='bold'
    )

    plt.tight_layout(pad=0)
    fig.patch.set_facecolor("#F5F5DC")

    canvas = FigureCanvasTkAgg(fig, master=frame5)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.configure(bg="#F5F5DC", highlightthickness=0)
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    if time_taken is not None and number_of_colors is not None:
        info_label = tk.Label(
            frame5,
            text=f"Time taken: {time_taken:.6f} seconds\nNumber of colors used: {number_of_colors}",
            bg="#F5F5DC",
            fg="#6082B6",
            font=("Arial", 14, "bold")
        )
        info_label.pack(pady=(10, 20))
