from catalog.domain.entities import Product


class AdminCreateProductUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(
        self,
        name: str,
        slug: str,
        description: str,
        price: float,
        category_slug: str,
        stock_quantity: int,
        image_url: str | None = None,
    ) -> Product:
        category = self.repository.get_category_by_slug(category_slug)
        if not category:
            raise ValueError("Category not found")

        product = Product.create(
            name=name,
            slug=slug,
            description=description,
            price=price,
            category_id=category.id,
            stock_quantity=stock_quantity,
            image_url=image_url,
        )
        return self.repository.save_product(product)
