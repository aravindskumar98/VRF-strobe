import asyncio
import random
from typing import List, Dict
from collections import defaultdict
import sympy
from utils import *
import math
from setup import setup, gen
import socket
import json
from gui import NodeGUI
import time

NUM_NODES = 8
MIN_MSGS_TO_SEND = 4

class Beacon:
    def __init__(self, x_0, N, s):
        self.latest_x_curr = x_0
        self.highest_round_num = 0
        self.N = N
        self.s = s

    def update_beacon(self, round_num, x_curr):
        if round_num > self.highest_round_num:
            print("Beacon updated")
            self.highest_round_num = round_num
            self.latest_x_curr = x_curr

    def get_latest_x_curr(self):
        return self.latest_x_curr

    def get_highest_round_num(self):
        return self.highest_round_num
    
    def _verify(self, x_next, x_curr):
        x_curr %= self.N
        if x_curr == pow(x_next, self.s, self.N):
            return True
        return False

class Node:
    def __init__(self, id, gui, beacon):
        self.id = id
        self.rounds_received = defaultdict(set)
        self.beacon = beacon
        self.current_round = 0
        self.received_messages_count = 0
        self.gui = gui
        self.time_taken_per_round = [-1]
        self.data_received_per_round = [-1]
        self.round_start_time = 0

    # Update the GUI when a new round is reached
    def update_gui(self):
        self.gui.update_node_info(self.id, self.current_round, self.x_curr, self.time_taken_per_round[-1], self.data_received_per_round[-1], self.beacon)

    def add_params(self, n, phi, N, s, a_coeff, x_0):
        self.N = N
        self.s = s
        self.n = n
        v = sympy.mod_inverse(math.factorial(n)*s, phi//4)
        self.sk = v + sum([a_coeff[j-1]*(self.id+1)**j for j in range(1, len(a_coeff)+1)])
        self.x_curr = x_0

    def _eval(self):
        x_next_i = pow(self.x_curr, self.sk, self.N)
        return x_next_i

    def _verify_share(self, x_next_i, x_curr_i):
        x_curr_i %= self.N
        if x_curr_i == pow(x_next_i, self.s, self.N):
            return True
        return False

    def _combine(self, x_next_array, selected_indices):
        n_fact = math.factorial(self.n)
        n_fact_times_L_0 = {i: lagrange_basis_polynomial(i, 0, selected_indices, n_fact) for i in range(1, self.n+1)}
        x_next = 1
        for i in selected_indices:
            x_next *= pow(x_next_array[i], n_fact_times_L_0[i], self.N)
        x_next %= self.N
        return x_next

    def _verify(self, x_next, x_curr):
        x_curr %= self.N
        if x_curr == pow(x_next, self.s, self.N):
            return True
        return False
    
    async def periodic_check(self):
        while True:
            if self.current_round < self.beacon.get_highest_round_num() - 5:
                self.current_round = self.beacon.get_highest_round_num()
                self.x_curr = self.beacon.get_latest_x_curr()
                print(f"Node {self.id} updated its state to match the beacon")
                self.update_gui()
            await asyncio.sleep(5)  # Check every 5 seconds


    async def start(self):
        server = await asyncio.start_server(self.server_callback, 'localhost', 8000 + self.id)
        self.round_start_time = time.time()
        self.data_received_in_bytes = 0
        async with server:
            await asyncio.gather(
                asyncio.create_task(self.send_messages()),
                asyncio.create_task(self.periodic_check()),
            )

    async def send_messages(self):
        await asyncio.sleep(1)  # Wait for all nodes to start

        while True:
            msg = {"sender": self.id, "round": self.current_round, "x_part": self._eval()}
            options = [i for i in range(NUM_NODES) if i != self.id]
            random.shuffle(options)
            for i in options:
                if i != self.id:
                    await self.send_message_to_socket(i, msg)
                    await asyncio.sleep(random.uniform(0.1, 0.5))  # Add random small delay

            await asyncio.sleep(0.1)  # Wait for the next round

    async def send_message_to_socket(self, target_id, message):
        try:
            reader, writer = await asyncio.open_connection(f'localhost', 8000 + target_id)
            writer.write(json.dumps(message).encode())
            await writer.drain()
            writer.close()
            await writer.wait_closed()
        except ConnectionRefusedError:
            pass

    async def server_callback(self, reader, writer):
        data = await reader.read(100)
        self.data_received_in_bytes += len(data)
        msg = json.loads(data.decode())

        round_num = msg["round"]
        msg_sender = msg["sender"]
        x_part = msg["x_part"]
        self.received_messages_count += 1

        if round_num == self.current_round:
            self.rounds_received[round_num].add((msg_sender+1, x_part))

            if len(self.rounds_received[round_num]) >= MIN_MSGS_TO_SEND:
                senders = [x[0] for x in self.rounds_received[round_num]]
                x_next_array = {x[0]: x[1] for x in self.rounds_received[round_num]}
                x_next = self._combine(x_next_array, senders)
                if self._verify(x_next, self.x_curr):
                    print(f"Node {self.id} verified the share")
                    self.x_curr = x_next
                    self.beacon.update_beacon(self.current_round, self.x_curr)
                else:
                    print(f"Node {self.id} failed to verify the share")
                
                self.current_round += 1
                print(f"Reached round {self.current_round} for node {self.id} -> Message = {self.x_curr}")
                current_time = time.time()
                self.time_taken_per_round.append(current_time - self.round_start_time)
                self.data_received_per_round.append(self.data_received_in_bytes)
                self.data_received_in_bytes = 0
                self.round_start_time = current_time
                self.update_gui()

        writer.close()
        await writer.wait_closed()

async def main():

    n = NUM_NODES
    t = MIN_MSGS_TO_SEND

    N, phi, s, a_coeff = setup(n,t)

    x_0 = gen(math.factorial(n), N)

    gui = NodeGUI(n)
    beacon = Beacon(x_0, N, s)

    nodes = [Node(i, gui, beacon) for i in range(NUM_NODES)]
    for node in nodes:
        node.add_params(n, phi, N, s, a_coeff, x_0)

    tasks = [node.start() for node in nodes] + [update_gui_periodically(gui)]

    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
