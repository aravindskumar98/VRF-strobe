import tkinter as tk
from tkinter import ttk

class NodeGUI:
    def __init__(self, n):
        self.n = n
        self.root = tk.Tk()
        self.root.title("Node Information")
        self.nodes = {}
        self.beacon_info = None
        self.create_widgets()

    def create_widgets(self):
        # self.root.geometry("1600x400")

        header = ttk.Label(self.root, text="Strobe - Minimal Simulation", font=("Arial", 24))
        header.grid(column=0, row=0, padx=10, pady=10)

        self.node_frame = ttk.Frame(self.root)
        self.node_frame.grid(column=0, row=1, padx=10, pady=10)

        self.create_node_labels()

    def create_node_labels(self):
        label = ttk.Label(self.node_frame, text=f"Beacon: Round 0 - Random Number: N/A", font=("Arial", 14))
        label.grid(column=0, row=0, padx=5, pady=5)
        self.beacon_info = label
        for i in range(self.n):
            label = ttk.Label(self.node_frame, text=f"Node {i}: Round 0 - Random Number: N/A", font=("Arial", 14))
            label.grid(column=0, row=i+1, padx=5, pady=5)
            self.nodes[i] = label

    def update_node_info(self, node_id, round_num, rand_num, prev_round_time, data_received, beacon = None):
        # if beacon not none, print Beacon present in Green font color
        if beacon is not None:
            self.beacon_info.config(text=f"Round {beacon.highest_round_num} - Random Number: {beacon.latest_x_curr}", foreground="green")
        self.nodes[node_id].config(text=f"Node {node_id}: Round {round_num} - Random Number: {rand_num} - Time Taken: {prev_round_time:.3f} sec - Data Received: {data_received} bytes")        


    def update(self):
        self.root.update()
