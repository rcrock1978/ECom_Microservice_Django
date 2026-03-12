from dataclasses import dataclass


@dataclass
class OrderCreatedEvent:
    order_number: str
    user_id: str


@dataclass
class OrderConfirmedEvent:
    order_number: str
    user_id: str
    total_amount: float
