from utils import prompt_gemini
import time


class Agent:
    def __init__(self, name, model):
        self.name = name
        self.model = model
        self.bus = None

    def send(self, receiver, content, msg_type="message.create", intent="chat"):
        msg = {
            "type": msg_type,
            "sender": self.name,
            "receiver": receiver,
            "content": content,
            "timestamp": time.time(),
            "metadata": {"intent": intent},
        }
        self.bus.send(msg)

    def receive(self, message):
        print(f"{self.name} <- {message['sender']}: {message['content']}")
        if message["content"].strip().upper() == "STOP":
            return
        formatted = "\n".join(
            [f"{m['sender']}: {m['content']}" for m in self.bus.history[-6:]]
        )
        reply = prompt_gemini(self.model, formatted + f"\n{self.name}:")
        print(f"{self.name} -> {message['receiver']}: {reply}")
        self.send(message["sender"], reply)
