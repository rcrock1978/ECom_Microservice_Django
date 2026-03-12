from collections.abc import Callable


class IdempotentConsumer:
    def __init__(self) -> None:
        self._processed: set[str] = set()

    def process(self, event_id: str, callback: Callable[[], None]) -> bool:
        if event_id in self._processed:
            return False
        callback()
        self._processed.add(event_id)
        return True


class RetryPolicy:
    def __init__(self, max_retries: int = 3) -> None:
        self.max_retries = max_retries

    def run(self, callback: Callable[[], None]) -> bool:
        attempts = 0
        while attempts <= self.max_retries:
            try:
                callback()
                return True
            except Exception:
                attempts += 1
        return False


class ConsumerRegistry:
    def __init__(self) -> None:
        self._handlers: dict[str, Callable[[object], None]] = {}

    def register(self, routing_key: str, handler: Callable[[object], None]) -> None:
        self._handlers[routing_key] = handler

    def resolve(self, routing_key: str) -> Callable[[object], None] | None:
        return self._handlers.get(routing_key)
