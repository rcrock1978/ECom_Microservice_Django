def serialize_cart(cart: object) -> dict[str, object]:
    items = []
    for item in getattr(cart, "items", []):
        items.append(
            {
                "id": item.id,
                "product_id": item.product_id,
                "product_name": item.product_name,
                "product_price": f"{item.product_price:.2f}",
                "quantity": item.quantity,
                "line_total": f"{item.line_total:.2f}",
            }
        )

    return {
        "id": getattr(cart, "id"),
        "user_id": getattr(cart, "user_id"),
        "items": items,
        "coupon_code": getattr(cart, "coupon_code", None),
        "item_count": getattr(cart, "item_count"),
        "subtotal": f"{getattr(cart, 'subtotal'):.2f}",
    }
