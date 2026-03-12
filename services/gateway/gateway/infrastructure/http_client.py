class InMemoryUpstreamClient:
    def __init__(self, availability: dict[str, bool] | None = None) -> None:
        self.availability = availability or {}

    def forward(self, upstream: str, path: str, method: str, headers: dict[str, str]) -> dict[str, object]:
        if self.availability.get(upstream, True) is False:
            return {"status": 503, "error": {"code": "UPSTREAM_UNAVAILABLE", "message": "Service unavailable"}}
        return {"status": 200, "data": {"path": path, "method": method, "upstream": upstream, "headers": headers}}
