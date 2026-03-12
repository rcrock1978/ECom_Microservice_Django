class AdminDeleteProductUseCase:
    def __init__(self, repository: object, pending_order_checker) -> None:
        self.repository = repository
        self.pending_order_checker = pending_order_checker

    def execute(self, slug: str) -> None:
        product = self.repository.get_product_by_slug(slug)
        if not product:
            raise ValueError("Product not found")

        if self.pending_order_checker(slug) > 0:
            raise PermissionError("Product has pending orders")

        product.is_active = False
        self.repository.save_product(product)
