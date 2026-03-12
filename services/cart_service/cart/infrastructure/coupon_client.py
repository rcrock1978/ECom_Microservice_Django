class CouponClient:
    def validate(self, coupon_code: str, subtotal: float) -> dict[str, object]:
        return {
            "is_valid": bool(coupon_code),
            "coupon_code": coupon_code,
            "subtotal": subtotal,
        }
