def serialize_product(product: object) -> dict[str, object]:
    return {
        "id": getattr(product, "id"),
        "name": getattr(product, "name"),
        "slug": getattr(product, "slug"),
        "description": getattr(product, "description"),
        "price": f"{getattr(product, 'price'):.2f}",
        "category_id": getattr(product, "category_id"),
        "stock_quantity": getattr(product, "stock_quantity"),
        "is_in_stock": getattr(product, "is_in_stock"),
        "image_url": getattr(product, "image_url", None),
    }


def serialize_category(category: object) -> dict[str, object]:
    return {
        "id": getattr(category, "id"),
        "name": getattr(category, "name"),
        "slug": getattr(category, "slug"),
        "description": getattr(category, "description", None),
        "parent_id": getattr(category, "parent_id", None),
    }
