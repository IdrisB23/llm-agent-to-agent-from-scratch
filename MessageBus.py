"""A simple message bus for inter-agent communication."""

class MessageBus:
    def __init__(self):
        self.history = []
        self.agents = {}

    def register(self, agent):
        self.agents[agent.name] = agent
        agent.bus = self

    def send(self, message):
        self.history.append(message)
        receiver_name = message["receiver"]
        if receiver_name in self.agents:
            self.agents[receiver_name].receive(message)
        else:
            print(f"[WARN] Receiver {receiver_name} not found")

    def broadcast(self, message):
        self.history.append(message)
        for agent in self.agents.values():
            if agent.name != message["sender"]:
                agent.receive(message)