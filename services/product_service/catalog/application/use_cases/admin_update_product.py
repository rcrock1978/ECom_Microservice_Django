class AdminUpdateProductUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, slug: str, **fields):
        product = self.repository.get_product_by_slug(slug)
        if not product:
            raise ValueError("Product not found")

        for key, value in fields.items():
            if value is not None and hasattr(product, key):
                setattr(product, key, value)

        return self.repository.save_product(product)
