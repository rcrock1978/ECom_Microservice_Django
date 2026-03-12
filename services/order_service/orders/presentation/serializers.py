def serialize_order_item(item: object) -> dict[str, object]:
    return {
        "id": getattr(item, "id"),
        "product_id": getattr(item, "product_id"),
        "product_name": getattr(item, "product_name"),
        "unit_price": f"{getattr(item, 'unit_price'):.2f}",
        "quantity": getattr(item, "quantity"),
        "line_total": f"{getattr(item, 'line_total'):.2f}",
    }


def serialize_order(order: object) -> dict[str, object]:
    return {
        "id": getattr(order, "id"),
        "order_number": getattr(order, "order_number"),
        "user_id": getattr(order, "user_id"),
        "status": getattr(order, "status"),
        "items": [serialize_order_item(item) for item in getattr(order, "items")],
        "subtotal": f"{getattr(order, 'subtotal'):.2f}",
        "discount_amount": f"{getattr(order, 'discount_amount'):.2f}",
        "total_amount": f"{getattr(order, 'total_amount'):.2f}",
        "email": getattr(order, "email", None),
    }
