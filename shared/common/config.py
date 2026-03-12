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


def load_common_settings(service_name: str) -> CommonSettings:
    return CommonSettings(
        service_name=service_name,
        debug=os.getenv("DJANGO_DEBUG", "False").lower() == "true",
        database_host=os.getenv("DATABASE_HOST", "localhost"),
        database_port=int(os.getenv("DATABASE_PORT", "5432")),
        rabbitmq_url=os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/"),
        redis_url=os.getenv("REDIS_URL", "redis://localhost:6379/0"),
    )
