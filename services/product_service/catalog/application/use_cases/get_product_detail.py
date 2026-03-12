class GetProductDetailUseCase:
    def __init__(self, product_repository: object) -> None:
        self.product_repository = product_repository

    def execute(self, slug: str) -> object:
        product = self.product_repository.get_product_by_slug(slug)
        if not product:
            raise ValueError("Product not found")
        return product
