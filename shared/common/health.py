from datetime import datetime, UTC


def build_health_payload(service: str, status: str = "ok") -> dict[str, str]:
    return {
        "service": service,
        "status": status,
        "timestamp": datetime.now(UTC).isoformat(),
    }
