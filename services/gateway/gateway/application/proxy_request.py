from gateway.domain.rate_limits import limit_for_path
from gateway.domain.routes import match_route


class ProxyRequestUseCase:
    def __init__(self, http_client: object, jwt_validator: object, rate_limiter: object) -> None:
        self.http_client = http_client
        self.jwt_validator = jwt_validator
        self.rate_limiter = rate_limiter

    def execute(self, path: str, method: str, access_token: str | None = None) -> dict[str, object]:
        route = match_route(path)
        if not route:
            return {"status": 404, "error": {"code": "ROUTE_NOT_FOUND", "message": "Route not found"}}

        route_limit = limit_for_path(path)
        rate_key = f"{method}:{path}:{access_token or 'anon'}"
        if not self.rate_limiter.allow(rate_key, route_limit):
            return {"status": 429, "error": {"code": "RATE_LIMITED", "message": "Too many requests"}}

        forwarded_headers: dict[str, str] = {"X-Request-ID": "request-id-stub"}
        if route["auth_required"]:
            validation = self.jwt_validator.validate(access_token)
            if not validation["is_valid"]:
                return {"status": 401, "error": {"code": "UNAUTHORIZED", "message": "Authentication required"}}
            claims = validation["claims"]
            forwarded_headers.update(
                {
                    "X-User-ID": claims.get("user_id", ""),
                    "X-User-Role": claims.get("role", "customer"),
                    "X-User-Email": claims.get("email", ""),
                }
            )

        upstream_response = self.http_client.forward(route["upstream"], path, method, forwarded_headers)
        return {
            "status": upstream_response["status"],
            "data": upstream_response.get("data", {}),
            "forwarded_headers": forwarded_headers,
        }
