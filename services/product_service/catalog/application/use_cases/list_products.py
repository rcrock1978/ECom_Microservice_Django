class ListProductsUseCase:
    def __init__(self, product_repository: object) -> None:
        self.product_repository = product_repository

    def execute(self, in_stock: bool | None = None) -> list[object]:
        return self.product_repository.list_products(in_stock=in_stock)
