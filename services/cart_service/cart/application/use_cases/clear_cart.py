class ClearCartUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str):
        cart = self.repository.get_by_user_id(user_id)
        if not cart:
            return None
        cart.items = []
        cart.coupon_code = None
        return self.repository.save(cart)
