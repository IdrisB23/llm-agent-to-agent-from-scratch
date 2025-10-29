"""A base class for message buses."""

from abc import ABC, abstractmethod
from models.Message import Message

class BaseBus(ABC):
    """Abstract base class for message buses."""

    @abstractmethod
    def register(self, agent_name: str, inbox_queue):
        pass

    @abstractmethod
    def send(self, message: Message):
        pass

    @abstractmethod
    def broadcast(self, message: Message):
        pass

    @abstractmethod
    def shutdown(self):
        pass
