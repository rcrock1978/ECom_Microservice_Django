from gateway.application.health_summary import HealthSummaryUseCase
from gateway.application.proxy_request import ProxyRequestUseCase
from gateway.infrastructure.http_client import InMemoryUpstreamClient
from gateway.infrastructure.jwt_validator import JwtValidator
from gateway.infrastructure.rate_limiter import InMemoryRateLimiter
from routing import ServiceRegistry


class GatewayFacade:
    def __init__(self) -> None:
        self.proxy_use_case = ProxyRequestUseCase(
            http_client=InMemoryUpstreamClient(),
            jwt_validator=JwtValidator(),
            rate_limiter=InMemoryRateLimiter(),
        )
        self.health_use_case = HealthSummaryUseCase(ServiceRegistry())

    @classmethod
    def in_memory(cls) -> "GatewayFacade":
        return cls()

    def proxy(self, path: str, method: str = "GET", access_token: str | None = None) -> dict[str, object]:
        return self.proxy_use_case.execute(path=path, method=method, access_token=access_token)

    def health(self) -> dict[str, object]:
        return self.health_use_case.execute()
