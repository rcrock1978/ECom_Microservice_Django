class GetOrderUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, order_number: str):
        order = self.repository.get_by_order_number(order_number)
        if not order:
            raise ValueError("Order not found")
        return order
