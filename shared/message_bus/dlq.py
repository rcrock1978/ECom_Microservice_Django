from dataclasses import dataclass


@dataclass(slots=True)
class DeadLetterMessage:
    event_id: str
    reason: str


def create_dead_letter(event_id: str, reason: str) -> DeadLetterMessage:
    return DeadLetterMessage(event_id=event_id, reason=reason)
