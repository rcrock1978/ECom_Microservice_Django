from orders.application.use_cases.cancel_order import CancelOrderUseCase
from orders.application.use_cases.create_order import CreateOrderUseCase
from orders.application.use_cases.get_order import GetOrderUseCase
from orders.application.use_cases.handle_payment_webhook import HandlePaymentWebhookUseCase
from orders.application.use_cases.list_orders import ListOrdersUseCase
from orders.application.use_cases.update_order_status import UpdateOrderStatusUseCase
from orders.infrastructure.event_publisher import OrderEventPublisher
from orders.infrastructure.payment_provider import PaymentProvider
from orders.infrastructure.repositories import InMemoryOrderRepository
from orders.presentation.serializers import serialize_order


class OrderFacade:
    def __init__(self, repository: InMemoryOrderRepository) -> None:
        self.repository = repository
        self.event_publisher = OrderEventPublisher()
        self.payment_provider = PaymentProvider()
        self.create_uc = CreateOrderUseCase(repository, self.event_publisher)
        self.list_uc = ListOrdersUseCase(repository)
        self.get_uc = GetOrderUseCase(repository)
        self.cancel_uc = CancelOrderUseCase(repository)
        self.webhook_uc = HandlePaymentWebhookUseCase(repository, self.payment_provider, self.event_publisher)
        self.update_status_uc = UpdateOrderStatusUseCase(repository)

    @classmethod
    def in_memory(cls) -> "OrderFacade":
        return cls(InMemoryOrderRepository())

    def create_order(
        self,
        user_id: str,
        items: list[dict[str, object]],
        discount_amount: float = 0,
        email: str | None = None,
    ) -> dict[str, object]:
        order = self.create_uc.execute(user_id=user_id, items=items, discount_amount=discount_amount, email=email)
        return {"status": 201, "data": serialize_order(order)}

    def list_orders(self, user_id: str) -> dict[str, object]:
        orders = self.list_uc.execute(user_id)
        return {"status": 200, "data": [serialize_order(order) for order in orders]}

    def get_order(self, order_number: str) -> dict[str, object]:
        order = self.get_uc.execute(order_number)
        return {"status": 200, "data": serialize_order(order)}

    def cancel_order(self, order_number: str) -> dict[str, object]:
        order = self.cancel_uc.execute(order_number)
        return {"status": 200, "data": serialize_order(order)}

    def handle_payment_webhook(self, order_number: str, provider_status: str) -> dict[str, object]:
        order = self.webhook_uc.execute(order_number, provider_status)
        return {"status": 200, "data": serialize_order(order)}

    def update_order_status(self, order_number: str, status: str) -> dict[str, object]:
        order = self.update_status_uc.execute(order_number, status)
        return {"status": 200, "data": serialize_order(order)}
