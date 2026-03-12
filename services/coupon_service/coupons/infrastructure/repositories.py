from coupons.domain.entities import Coupon, CouponUsage


class InMemoryCouponRepository:
    def __init__(self) -> None:
        self.coupons: dict[str, Coupon] = {}
        self.usages: list[CouponUsage] = []

    def get_by_code(self, code: str) -> Coupon | None:
        return self.coupons.get(code.upper())

    def save(self, coupon: Coupon) -> Coupon:
        self.coupons[coupon.code.upper()] = coupon
        return coupon

    def list(self, active_only: bool = False) -> list[Coupon]:
        values = list(self.coupons.values())
        if not active_only:
            return values
        return [coupon for coupon in values if coupon.is_active]

    def add_usage(self, usage: CouponUsage) -> None:
        self.usages.append(usage)
