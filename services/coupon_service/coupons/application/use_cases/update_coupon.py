class UpdateCouponUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, code: str, **fields):
        coupon = self.repository.get_by_code(code)
        if not coupon:
            raise ValueError("Coupon not found")

        for key, value in fields.items():
            if value is not None and hasattr(coupon, key):
                setattr(coupon, key, value)

        return self.repository.save(coupon)
