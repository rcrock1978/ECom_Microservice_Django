from dataclasses import dataclass


@dataclass(slots=True)
class MessageBusConfig:
    exchange_name: str = "mango.events"
    dead_letter_exchange: str = "mango.events.dlq"
    max_retries: int = 3
