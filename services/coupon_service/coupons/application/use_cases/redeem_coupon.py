from coupons.domain.entities import CouponUsage


class RedeemCouponUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, code: str, user_id: str):
        coupon = self.repository.get_by_code(code)
        if not coupon:
            raise ValueError("Coupon not found")

        coupon.mark_redeemed()
        self.repository.save(coupon)
        self.repository.add_usage(CouponUsage.create(coupon_id=coupon.id, user_id=user_id))
        return coupon
