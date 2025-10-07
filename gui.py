import tkinter as tk
from tkinter import messagebox
from algorithms import genetics_algo, solve
from config import set_of_colors

def show_next_page5(frame_dell, num_nodes, edges, list1, root):
    frame_dell.pack_forget()
    frame4 = tk.Frame(root, bg="#F5F5DC")
    frame4.pack()

    entries = {}

    for text in ["Population size:", "Number of generations:", "Mutation rate:", "Crossover probability:", "Retain probability:"]:
        label = tk.Label(frame4, text=text, bg="#6082B6", fg="white", font=("Arial", 12, "bold"))
        label.pack(pady=(10, 5))
        entry = tk.Entry(frame4, width=15, bg="#FDFBD4", fg="#6082B6", font=("Arial", 12))
        entry.pack(pady=(5, 10))
        entries[text] = entry

    def submit():
        genetics_algo(
            frame4,
            int(entries["Population size:"].get()),
            int(entries["Number of generations:"].get()),
            float(entries["Mutation rate:"].get()),
            float(entries["Crossover probability:"].get()),
            float(entries["Retain probability:"].get()),
            num_nodes, edges, list1, root
        )

    tk.Button(frame4, text="OK", command=submit, bg="#6082B6", fg="white", font=("Arial", 12, "bold")).pack(pady=20)

def show_algorithm_selection(num_nodes, edges, list1, root):
    frame3 = tk.Frame(root, bg="#F5F5DC")
    frame3.pack()

    choice = tk.Label(frame3, text="Choose which algorithm to use", bg="#6082B6", fg="white", font=("Arial", 18, "bold"))
    choice.pack(pady=(90,20))

    tk.Button(frame3, text="Backtracking Search Algorithm", command=lambda: solve(num_nodes, edges, frame3, list1, root),
              bg="#6082B6", fg="white", font=("Arial", 14, "bold")).pack(pady=(10,20))

    tk.Button(frame3, text="Genetics Algorithm", command=lambda: show_next_page5(frame3, num_nodes, edges, list1, root),
              bg="#6082B6", fg="white", font=("Arial", 14, "bold")).pack(pady=(10,20))
