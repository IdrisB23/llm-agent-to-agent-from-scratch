import datetime
from agent.ThreadAgent import AgentThread
from bus.ThreadBus import ThreadBus
import time

from models.Message import Message


bus = ThreadBus()

def handler_A(msg: Message, history):
    # your agent logic, call LLM etc.
    time.sleep(1)  # simulate processing time
    return f"Reply to {msg.content}"

def handler_B(msg: Message, history):
    # your agent logic, call LLM etc.
    time.sleep(1)  # simulate processing time
    return f"Test {msg.content}"

a = AgentThread("Agent A", bus, handler_A)
b = AgentThread("Agent B", bus, handler_B)
a.start()
b.start()

# keep main thread alive. Take user input to send messages.
while True:
    user_input =input("Send a message (press Enter)...")
    # shutdown on "exit"
    if user_input.strip().lower() == "exit":
        bus.shutdown()
        a.join()
        b.join()
        break
    msg = Message(
        type="message.create",
        sender="Agent A",
        recipient="Agent B",
        timestamp=datetime.datetime.now(),
        content=user_input,
        metadata={},
    )
    bus.send(msg)