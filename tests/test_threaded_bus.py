"""Tests for the ThreadBus implementation."""

import time
from agent.ThreadAgent import AgentThread
from bus.ThreadBus import ThreadBus 
from models.Message import Message

def test_send_receive_shutdown():
    bus = ThreadBus()

    received = []

    def handler(msg, history):
        received.append(msg.content)
        return "ok"

    a = AgentThread("A", bus, handler)
    b = AgentThread("B", bus, handler)

    a.start()
    b.start()

    msg = Message(type="message.create", sender="A", recipient="B", content="hi")
    bus.send(msg)
    time.sleep(0.5)

    assert "hi" in received

    bus.shutdown()
    a.join(2)
    b.join(2)
    assert not a.is_alive() and not b.is_alive()
