from dataclasses import asdict
from .events import EventEnvelope


class MessagePublisher:
    def publish(self, event: EventEnvelope, routing_key: str) -> dict[str, str]:
        _ = asdict(event)
        return {"status": "queued", "routing_key": routing_key, "event_id": event.event_id}
