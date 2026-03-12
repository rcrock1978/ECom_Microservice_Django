class CartClient:
    def get_cart(self, user_id: str) -> dict[str, object]:
        return {"user_id": user_id, "items": []}


class ProductClient:
    def get_product(self, product_id: str) -> dict[str, object]:
        return {"id": product_id, "name": "Sample Product", "price": 99.0}


class CouponClient:
    def validate_coupon(self, code: str, subtotal: float) -> dict[str, object]:
        if code.upper() == "SAVE10" and subtotal >= 100:
            return {"is_valid": True, "discount_amount": 10.0}
        return {"is_valid": False, "discount_amount": 0.0}


class RewardClient:
    def validate_redemption(self, user_id: str, points: int) -> dict[str, object]:
        return {"user_id": user_id, "points": points, "is_valid": points <= 100}
