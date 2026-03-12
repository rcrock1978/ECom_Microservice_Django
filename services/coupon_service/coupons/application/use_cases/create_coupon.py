from coupons.domain.entities import Coupon


class CreateCouponUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(
        self,
        code: str,
        discount_type: str,
        discount_value: float,
        min_order_amount: float = 0,
        max_discount_amount: float | None = None,
        usage_limit: int | None = None,
    ) -> Coupon:
        coupon = Coupon.create(
            code=code,
            discount_type=discount_type,
            discount_value=discount_value,
            min_order_amount=min_order_amount,
            max_discount_amount=max_discount_amount,
            usage_limit=usage_limit,
        )
        return self.repository.save(coupon)
