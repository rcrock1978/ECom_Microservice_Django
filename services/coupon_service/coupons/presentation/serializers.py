def serialize_coupon(coupon: object) -> dict[str, object]:
    return {
        "id": getattr(coupon, "id"),
        "code": getattr(coupon, "code"),
        "discount_type": getattr(coupon, "discount_type"),
        "discount_value": f"{getattr(coupon, 'discount_value'):.2f}",
        "min_order_amount": f"{getattr(coupon, 'min_order_amount'):.2f}",
        "max_discount_amount": (
            f"{getattr(coupon, 'max_discount_amount'):.2f}" if getattr(coupon, "max_discount_amount") is not None else None
        ),
        "usage_limit": getattr(coupon, "usage_limit"),
        "used_count": getattr(coupon, "used_count"),
        "is_active": getattr(coupon, "is_active"),
    }
