class ApplyCouponUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str, coupon_code: str):
        cart = self.repository.get_by_user_id(user_id)
        if not cart:
            raise ValueError("Cart not found")
        cart.apply_coupon(coupon_code)
        return self.repository.save(cart)
