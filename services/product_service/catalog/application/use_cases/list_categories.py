class ListCategoriesUseCase:
    def __init__(self, category_repository: object) -> None:
        self.category_repository = category_repository

    def execute(self) -> list[object]:
        return self.category_repository.list_categories()
