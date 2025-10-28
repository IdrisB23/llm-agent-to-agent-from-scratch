from threads.ThreadAgent import AgentThread
from threads.ThreadBus import ThreadBus
import time


bus = ThreadBus()

def handler_A(msg, history):
    # your agent logic, call LLM etc.
    time.sleep(1)  # simulate processing time
    return f"Reply to {msg['content']}"

def handler_B(msg, history):
    # your agent logic, call LLM etc.
    time.sleep(1)  # simulate processing time
    return f"Test {msg['content']}"

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
    bus.send({"type":"message.create","sender":"Agent A","receiver":"Agent B","timestamp":time.time(),"content":user_input,"metadata":{}})