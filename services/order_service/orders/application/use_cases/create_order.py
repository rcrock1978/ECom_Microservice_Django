from orders.domain.entities import Order, OrderItem


class CreateOrderUseCase:
    def __init__(self, repository: object, event_publisher: object | None = None) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, user_id: str, items: list[dict[str, object]], discount_amount: float = 0, email: str | None = None) -> Order:
        order_items = [
            OrderItem.create(
                product_id=str(item["product_id"]),
                product_name=str(item["product_name"]),
                unit_price=float(item["unit_price"]),
                quantity=int(item["quantity"]),
            )
            for item in items
        ]
        order = Order.create(user_id=user_id, items=order_items, discount_amount=discount_amount, email=email)
        saved = self.repository.save(order)
        if self.event_publisher:
            self.event_publisher.publish_order_created(saved)
        return saved
