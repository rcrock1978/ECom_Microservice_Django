from dataclasses import dataclass, field, asdict
from datetime import datetime, UTC
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class EventEnvelope:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    version: str = "1.0"
    source: str = ""
    correlation_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BaseEvent(EventEnvelope):
    pass
