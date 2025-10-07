# main.py
import tkinter as tk
from gui import show_algorithm_selection
from utils import close_program

def main():
    edges = {}
    list1 = []
    root = tk.Tk()
    root.configure(bg="#F5F5DC")
    root.title("Color Graph Solver")
    
    window_width, window_height = 600, 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    frame1 = tk.Frame(root, bg="#F5F5DC")
    frame1.pack()

    tk.Label(frame1, text="Number of nodes:", bg="#6082B6", font=("Arial", 24, "bold italic"), fg="white").pack(pady=(120, 10))
    nodes_entry = tk.Entry(frame1, bg="#FDFBD4", fg="#6082B6", font=("Arial", 14))
    nodes_entry.pack(pady=(5, 10))

    tk.Label(frame1, text="Number of edges:", bg="#6082B6", font=("Arial", 20, "bold italic"), fg="white").pack(pady=(20, 10))
    edges_entry = tk.Entry(frame1, bg="#FDFBD4", fg="#6082B6", font=("Arial", 14))
    edges_entry.pack(pady=(5, 10))

    def start():
        num_nodes = int(nodes_entry.get())
        expected_edges = int(edges_entry.get())
        frame1.pack_forget()

        frame2 = tk.Frame(root, bg="#F5F5DC")
        frame2.pack()

        count = [0]

        def add_edge():
            n1 = node1_entry.get()
            n2 = node2_entry.get()
            if n1 and n2:
                list1.append((n1, n2))
                edges.setdefault(n1, []).append(n2)
                edges.setdefault(n2, []).append(n1)
                count[0] += 1
                node1_entry.delete(0, tk.END)
                node2_entry.delete(0, tk.END)
                if count[0] >= expected_edges:
                    frame2.pack_forget()
                    show_algorithm_selection(num_nodes, edges, list1, root)

        tk.Label(frame2, text="Node 1:", bg="#6082B6", fg="white", font=("Arial", 16, "bold")).pack(pady=(70, 5))
        node1_entry = tk.Entry(frame2, bg="#FDFBD4", fg="#6082B6", font=("Arial", 14))
        node1_entry.pack(pady=(10, 5))

        tk.Label(frame2, text="Node 2:", bg="#6082B6", fg="white", font=("Arial", 16, "bold")).pack(pady=(20, 5))
        node2_entry = tk.Entry(frame2, bg="#FDFBD4", fg="#6082B6", font=("Arial", 14))
        node2_entry.pack(pady=(10, 5))

        tk.Button(frame2, text="Add Edge", command=add_edge, bg="#6082B6", fg="white", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(frame1, text="OK", command=start, bg="#6082B6", fg="white", font=("Arial", 16, "bold italic")).pack(pady=20)
    root.protocol("WM_DELETE_WINDOW", close_program)
    root.mainloop()

if __name__ == "__main__":
    main()
