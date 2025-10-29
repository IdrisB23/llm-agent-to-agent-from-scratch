"""A simple message bus for inter-thread communication between agents."""

import datetime
import threading
import queue

from bus.BaseBus import BaseBus
from models.Message import Message

class ThreadBus(BaseBus):
    def __init__(self):
        self.queues = {} # agent_name -> Queue
        self.history = []
        self.history_lock = threading.RLock()
        self.agents = {} # agent_name -> Agent
        self.running = True

    def register(self, agent_name, q):
        self.queues[agent_name] = q

    def append_history(self, msg):
        # lock history for thread safety (race conditions)
        with self.history_lock:
            self.history.append(msg)

    def broadcast(self, msg: Message, timeout=1.0):
        for agent_name, q in self.queues.items():
            if agent_name != msg.sender:
                try:
                    q.put(msg, timeout=timeout)
                except queue.Full:
                    print(f"[WARN] queue full for {agent_name}")

    def send(self, msg: Message, timeout=1.0):
        print(f"[BUS] {msg.sender} -> {msg.recipient}: {msg.content}")
        receiver = msg.recipient
        self.append_history(msg)
        if receiver == "broadcast":
            self.broadcast(msg, timeout)
        else:
            q = self.queues.get(receiver)
            if q is None:
                print(f"[WARN] receiver {receiver} not found")
            else:
                try:
                    q.put(msg, timeout=timeout)
                except queue.Full:
                    print(f"[WARN] queue full for {receiver}")

    def shutdown(self):
        self.running = False
        # send shutdown control to every agent (broadcast)
        shutdown_msg = Message(
            type="control",
            sender="system",
            recipient="broadcast",
            timestamp=datetime.datetime.now(),
            content="SHUTDOWN",
        )
        self.send(shutdown_msg, timeout=0.1)
