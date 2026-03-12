class UpdateOrderStatusUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, order_number: str, status: str):
        order = self.repository.get_by_order_number(order_number)
        if not order:
            raise ValueError("Order not found")

        if status == "paid":
            order.mark_paid()
        elif status == "shipped":
            order.mark_shipped()
        elif status == "cancelled":
            order.cancel()
        else:
            order.status = status

        return self.repository.save(order)
