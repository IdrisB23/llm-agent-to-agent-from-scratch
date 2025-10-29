"""A simple threaded agent implementation for inter-thread communication."""

import threading
import queue
import datetime
from models.Message import Message


class AgentThread(threading.Thread):
    def __init__(self, name, bus, handler, queue_maxsize=100):
        super().__init__(daemon=True)
        self.name = name
        self.bus = bus
        self.inbox = queue.Queue(maxsize=queue_maxsize) # queue for incoming messages
        self.handler = handler # function to handle and respond to messages
        bus.register(self.name, self.inbox)
        self._stop_event = threading.Event()

    def run(self):
        while not self._stop_event.is_set():
            try:
                msg = self.inbox.get(timeout=1.0)
            except queue.Empty:
                continue
            # control messages
            if msg.type == "control" and msg.content == "SHUTDOWN":
                break
            # process message
            try:
                # handler uses bus.history if needed; history is protected by bus
                reply = self.handler(msg, self.bus.history)
                if reply is not None:
                    out_msg = Message(
                        type="message.create",
                        sender=self.name,
                        recipient=msg.sender,
                        timestamp=datetime.datetime.now(),
                        content=reply,
                        metadata={},
                    )
                    self.bus.send(out_msg)
            except Exception as e:
                print(f"[ERROR] agent {self.name}: {e}")
        print(f"{self.name} exiting")

    def stop(self):
        self._stop_event.set()
        # push a control message to unblock queue
        try:
            self.inbox.put_nowait(
                {
                    "type": "control",
                    "sender": "system",
                    "receiver": self.name,
                    "timestamp": datetime.datetime.now(),
                    "content": "SHUTDOWN",
                }
            )
        except queue.Full:
            pass
