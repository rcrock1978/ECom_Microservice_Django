from dataclasses import dataclass
from collections.abc import Callable


@dataclass(slots=True)
class DeadLetterMessage:
    event_id: str
    reason: str


def create_dead_letter(event_id: str, reason: str) -> DeadLetterMessage:
    return DeadLetterMessage(event_id=event_id, reason=reason)


class DeadLetterQueue:
    def __init__(self) -> None:
        self._messages: list[DeadLetterMessage] = []

    def push(self, event_id: str, reason: str) -> DeadLetterMessage:
        message = create_dead_letter(event_id=event_id, reason=reason)
        self._messages.append(message)
        return message

    def inspect(self) -> list[DeadLetterMessage]:
        return list(self._messages)

    def replay(self, callback: Callable[[DeadLetterMessage], bool]) -> int:
        remaining: list[DeadLetterMessage] = []
        replayed = 0
        for message in self._messages:
            if callback(message):
                replayed += 1
            else:
                remaining.append(message)
        self._messages = remaining
        return replayed
