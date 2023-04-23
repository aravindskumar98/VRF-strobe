import asyncio
import random
from typing import List, Dict
from collections import defaultdict

NUM_NODES = 8
MIN_MSGS_TO_SEND = 4

class Node:
    def __init__(self, id: int, message_queues: List[asyncio.Queue]):
        self.id = id
        self.message_queues = message_queues
        self.rounds_received = defaultdict(set)
        self.current_round = 0
        self.received_messages_count = 0
        self.curr_message = ""

    async def start(self):
        await asyncio.gather(
            asyncio.create_task(self.receive_messages()),
            asyncio.create_task(self.send_messages())
        )

    async def send_messages(self):
        await asyncio.sleep(1)  # Wait for all nodes to start

        while True:
            msg = {"sender": str(self.id), "round": self.current_round}
            for i in range(NUM_NODES):
                if i != self.id:
                    await self.message_queues[i].put(msg)
                    await asyncio.sleep(random.uniform(1, 5))  # Add random small delay

            await asyncio.sleep(1)  # Wait for the next round

    async def receive_messages(self):
        while True:
            msg = await self.message_queues[self.id].get()
            round_num = msg["round"]
            msg_sender = msg["sender"]
            # print(f"Received message in node {self.id} from node {msg_sender} in round {round_num} : count {self.received_messages_count}")
            self.received_messages_count += 1

            if round_num == self.current_round:
                self.rounds_received[round_num].add(msg_sender)
                self.curr_message += msg_sender

                if len(self.rounds_received[round_num]) >= MIN_MSGS_TO_SEND:
                    # Increment the round and start sending new messages
                    self.current_round += 1
                    print(f"Reached round {self.current_round} for node {self.id}")
                    print(f"Message = {self.curr_message}")

async def main():
    message_queues = [asyncio.Queue() for _ in range(NUM_NODES)]
    nodes = [Node(i, message_queues) for i in range(NUM_NODES)]

    tasks = [node.start() for node in nodes]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
