from abc import ABC
from abc import abstractmethod


class QueueAdapterABC(ABC):
    """Provide a standard interface for queue adapters."""

    @abstractmethod
    def connect(self, *args, **kwargs):
        """Connect to the queue."""
        pass

    @abstractmethod
    def disconnect(self, *args, **kwargs):
        """Disconnect from the queue."""
        pass

    @abstractmethod
    def dispatch(self, *args, **kwargs):
        """Dispatch a message to the queue."""
        pass

    @abstractmethod
    def consume(self, *args, **kwargs):
        """Consume a message from the queue."""
        pass
