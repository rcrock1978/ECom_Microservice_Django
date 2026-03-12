class HandlePaymentWebhookUseCase:
    def __init__(self, repository: object, payment_provider: object, event_publisher: object | None = None) -> None:
        self.repository = repository
        self.payment_provider = payment_provider
        self.event_publisher = event_publisher

    def execute(self, order_number: str, provider_status: str):
        order = self.repository.get_by_order_number(order_number)
        if not order:
            raise ValueError("Order not found")

        if self.payment_provider.is_success(provider_status):
            order.mark_paid()
            saved = self.repository.save(order)
            if self.event_publisher:
                self.event_publisher.publish_order_confirmed(saved)
            return saved

        order.cancel()
        return self.repository.save(order)
