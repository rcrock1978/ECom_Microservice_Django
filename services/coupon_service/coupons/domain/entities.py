from dataclasses import dataclass
from uuid import uuid4


@dataclass
class Coupon:
    id: str
    code: str
    discount_type: str
    discount_value: float
    min_order_amount: float = 0.0
    max_discount_amount: float | None = None
    usage_limit: int | None = None
    used_count: int = 0
    is_active: bool = True

    @classmethod
    def create(
        cls,
        code: str,
        discount_type: str,
        discount_value: float,
        min_order_amount: float = 0.0,
        max_discount_amount: float | None = None,
        usage_limit: int | None = None,
    ) -> "Coupon":
        return cls(
            id=str(uuid4()),
            code=code.upper(),
            discount_type=discount_type,
            discount_value=float(discount_value),
            min_order_amount=float(min_order_amount),
            max_discount_amount=max_discount_amount,
            usage_limit=usage_limit,
        )

    def can_redeem(self) -> bool:
        if not self.is_active:
            return False
        if self.usage_limit is None:
            return True
        return self.used_count < self.usage_limit

    def mark_redeemed(self) -> None:
        if not self.can_redeem():
            raise ValueError("Coupon cannot be redeemed")
        self.used_count += 1

    def calculate_discount(self, subtotal: float) -> float:
        if not self.is_active or subtotal < self.min_order_amount:
            return 0.0

        if self.discount_type == "percentage":
            discount = subtotal * (self.discount_value / 100)
        else:
            discount = self.discount_value

        if self.max_discount_amount is not None:
            discount = min(discount, self.max_discount_amount)

        discount = max(discount, 0.0)
        return min(discount, subtotal)


@dataclass
class CouponUsage:
    id: str
    coupon_id: str
    user_id: str

    @classmethod
    def create(cls, coupon_id: str, user_id: str) -> "CouponUsage":
        return cls(id=str(uuid4()), coupon_id=coupon_id, user_id=user_id)
