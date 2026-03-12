class ValidateCouponUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, code: str, subtotal: float) -> dict[str, object]:
        coupon = self.repository.get_by_code(code)
        if not coupon or not coupon.can_redeem():
            return {"is_valid": False, "discount_amount": 0.0}

        discount_amount = coupon.calculate_discount(subtotal)
        return {"is_valid": discount_amount > 0, "discount_amount": discount_amount}
