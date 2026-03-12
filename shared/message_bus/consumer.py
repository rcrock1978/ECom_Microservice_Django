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
