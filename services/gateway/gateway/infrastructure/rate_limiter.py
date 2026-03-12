class InMemoryRateLimiter:
    def __init__(self) -> None:
        self._counts: dict[str, int] = {}

    def allow(self, key: str, limit: int) -> bool:
        current = self._counts.get(key, 0)
        if current >= limit:
            return False
        self._counts[key] = current + 1
        return True
