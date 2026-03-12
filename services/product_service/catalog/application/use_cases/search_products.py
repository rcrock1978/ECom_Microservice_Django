class SearchProductsUseCase:
    def __init__(self, product_repository: object) -> None:
        self.product_repository = product_repository

    def execute(self, query: str) -> list[object]:
        return self.product_repository.search_products(query)
