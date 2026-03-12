from shared.message_bus.events import OrderConfirmedEvent
from shared.message_bus.publisher import MessagePublisher


class OrderEventPublisher:
    def __init__(self, publisher: MessagePublisher | None = None) -> None:
        self.publisher = publisher or MessagePublisher()
        self.published: list[dict[str, str]] = []

    def publish_order_created(self, order: object) -> None:
        self.published.append({"type": "order.created", "order_number": getattr(order, "order_number")})

    def publish_order_confirmed(self, order: object) -> None:
        event = OrderConfirmedEvent.create(
            order_id=getattr(order, "order_number"),
            user_id=getattr(order, "user_id"),
            total=float(getattr(order, "total_amount")),
        )
        self.publisher.publish(event=event, routing_key="order.confirmed")
        self.published.append({"type": "order.confirmed", "order_number": getattr(order, "order_number")})
