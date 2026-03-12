class ProcessedEventStore:
    def __init__(self) -> None:
        self._processed_ids: set[str] = set()

    def is_processed(self, event_id: str) -> bool:
        return event_id in self._processed_ids

    def mark_processed(self, event_id: str) -> None:
        self._processed_ids.add(event_id)
