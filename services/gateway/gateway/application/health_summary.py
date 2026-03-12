class HealthSummaryUseCase:
    def __init__(self, registry: object) -> None:
        self.registry = registry

    def execute(self) -> dict[str, object]:
        return {"status": "ok", "services": self.registry.services()}
