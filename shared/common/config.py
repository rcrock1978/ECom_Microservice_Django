from dataclasses import dataclass
import os


@dataclass
class CommonSettings:
    service_name: str
    debug: bool
    database_host: str
    database_port: int
    rabbitmq_url: str
    redis_url: str
    secure_cookies: bool
    csrf_trusted_origins: list[str]
    service_auth_token: str


def load_common_settings(service_name: str) -> CommonSettings:
    return CommonSettings(
        service_name=service_name,
        debug=os.getenv("DJANGO_DEBUG", "False").lower() == "true",
        database_host=os.getenv("DATABASE_HOST", "localhost"),
        database_port=int(os.getenv("DATABASE_PORT", "5432")),
        rabbitmq_url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
        secure_cookies=os.getenv("SECURE_COOKIES", "True").lower() == "true",
        csrf_trusted_origins=[origin for origin in os.getenv("CSRF_TRUSTED_ORIGINS", "http://localhost:3000").split(",") if origin],
        service_auth_token=os.getenv("SERVICE_AUTH_TOKEN", "local-service-token"),
    )
