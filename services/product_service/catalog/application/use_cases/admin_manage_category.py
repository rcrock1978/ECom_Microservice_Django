from catalog.domain.entities import Category


class AdminManageCategoryUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def create(self, name: str, slug: str, description: str | None = None, parent_slug: str | None = None) -> Category:
        parent_id = None
        if parent_slug:
            parent = self.repository.get_category_by_slug(parent_slug)
            if not parent:
                raise ValueError("Parent category not found")
            parent_id = parent.id

        category = Category.create(name=name, slug=slug, description=description, parent_id=parent_id)
        return self.repository.save_category(category)

    def update(self, slug: str, **fields):
        category = self.repository.get_category_by_slug(slug)
        if not category:
            raise ValueError("Category not found")

        for key, value in fields.items():
            if value is not None and hasattr(category, key):
                setattr(category, key, value)

        return self.repository.save_category(category)
