from coupons.domain.entities import Coupon
from coupons.infrastructure.repositories import InMemoryCouponRepository


def seed_default_coupons(repository: InMemoryCouponRepository | None = None) -> InMemoryCouponRepository:
    repository = repository or InMemoryCouponRepository()
    repository.save(Coupon.create(code="SAVE10", discount_type="fixed", discount_value=10, min_order_amount=50))
    repository.save(Coupon.create(code="WELCOME15", discount_type="percentage", discount_value=15, min_order_amount=75))
    return repository
