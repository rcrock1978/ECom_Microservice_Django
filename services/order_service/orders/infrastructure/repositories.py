from orders.domain.entities import Order


class InMemoryOrderRepository:
    def __init__(self) -> None:
        self._orders: dict[str, Order] = {}

    def save(self, order: Order) -> Order:
        self._orders[order.order_number] = order
        return order

    def get_by_order_number(self, order_number: str) -> Order | None:
        return self._orders.get(order_number)

    def list_by_user_id(self, user_id: str) -> list[Order]:
        return [order for order in self._orders.values() if order.user_id == user_id]
