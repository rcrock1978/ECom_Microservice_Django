class ProductClient:
    def get_product(self, product_id: str) -> dict[str, object]:
        return {
            "id": product_id,
            "name": "Stub Product",
            "price": 10.0,
            "stock_quantity": 100,
            "is_active": True,
        }
