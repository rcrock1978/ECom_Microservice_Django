from abc import ABC, abstractmethod
from typing import Any, Dict, Callable, List

class MessageBus(ABC):
    """Abstract base for a simple publish/subscribe message bus."""

    @abstractmethod
    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        raise NotImplementedError

    @abstractmethod
    def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        raise NotImplementedError


class InMemoryMessageBus(MessageBus):
    """A naive in-memory implementation useful for local development and tests."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable[[Dict[str, Any]], None]]] = {}

    def publish(self, topic: str, message: Dict[str, Any]) -> None:
        for handler in self._subscribers.get(topic, []):
            handler(message)

    def subscribe(self, topic: str, handler: Callable[[Dict[str, Any]], None]) -> None:
        self._subscribers.setdefault(topic, []).append(handler)
