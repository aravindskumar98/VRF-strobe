import tkinter as tk
from tkinter import ttk

class NodeGUI:
    def __init__(self, n):
        self.n = n
        self.root = tk.Tk()
        self.root.title("Node Information")
        self.nodes = {}
        self.create_widgets()

    def create_widgets(self):
        header = ttk.Label(self.root, text="Node Information", font=("Arial", 24))
        header.grid(column=0, row=0, padx=10, pady=10)

        self.node_frame = ttk.Frame(self.root)
        self.node_frame.grid(column=0, row=1, padx=10, pady=10)

        self.create_node_labels()

    def create_node_labels(self):
        for i in range(self.n):
            label = ttk.Label(self.node_frame, text=f"Node {i}: Round 0 - Random Number: N/A", font=("Arial", 14))
            label.grid(column=0, row=i, padx=5, pady=5)
            self.nodes[i] = label

    def update_node_info(self, node_id, round_num, rand_num):
        self.nodes[node_id].config(text=f"Node {node_id}: Round {round_num} - Random Number: {rand_num}")

    def update(self):
        self.root.update()
