from coupons.domain.entities import Coupon, CouponUsage


class InMemoryCouponRepository:
    def __init__(self) -> None:
        self.coupons: dict[str, Coupon] = {}
        self.usages: list[CouponUsage] = []
        self._validation_cache: dict[tuple[str, bool], list[Coupon]] = {}

    def _invalidate_cache(self) -> None:
        self._validation_cache.clear()

    def get_by_code(self, code: str) -> Coupon | None:
        return self.coupons.get(code.upper())

    def save(self, coupon: Coupon) -> Coupon:
        self.coupons[coupon.code.upper()] = coupon
        self._invalidate_cache()
        return coupon

    def list(self, active_only: bool = False) -> list[Coupon]:
        cache_key = ("list", active_only)
        cached = self._validation_cache.get(cache_key)
        if cached is not None:
            return list(cached)
        values = list(self.coupons.values())
        if not active_only:
            self._validation_cache[cache_key] = list(values)
            return values
        filtered = [coupon for coupon in values if coupon.is_active]
        self._validation_cache[cache_key] = list(filtered)
        return filtered

    def add_usage(self, usage: CouponUsage) -> None:
        self.usages.append(usage)
