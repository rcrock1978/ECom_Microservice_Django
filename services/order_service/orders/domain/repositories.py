from typing import Protocol

from orders.domain.entities import Order


class OrderRepository(Protocol):
    def save(self, order: Order) -> Order: ...

    def get_by_order_number(self, order_number: str) -> Order | None: ...

    def list_by_user_id(self, user_id: str) -> list[Order]: ...
