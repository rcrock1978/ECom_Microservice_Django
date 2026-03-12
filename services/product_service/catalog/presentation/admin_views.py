from catalog.application.use_cases.admin_create_product import AdminCreateProductUseCase
from catalog.application.use_cases.admin_delete_product import AdminDeleteProductUseCase
from catalog.application.use_cases.admin_manage_category import AdminManageCategoryUseCase
from catalog.application.use_cases.admin_update_product import AdminUpdateProductUseCase
from catalog.domain.entities import Category, Product
from catalog.infrastructure.repositories import InMemoryCatalogRepository
from catalog.presentation.admin_serializers import serialize_category, serialize_product


class AdminCatalogFacade:
    def __init__(self, repository: InMemoryCatalogRepository, pending_orders_by_slug: dict[str, int] | None = None) -> None:
        self.repository = repository
        self.pending_orders_by_slug = pending_orders_by_slug or {}
        self.create_product_uc = AdminCreateProductUseCase(repository)
        self.update_product_uc = AdminUpdateProductUseCase(repository)
        self.delete_product_uc = AdminDeleteProductUseCase(repository, self._pending_order_count)
        self.manage_category_uc = AdminManageCategoryUseCase(repository)

    @classmethod
    def in_memory_seeded(cls, pending_orders_by_slug: dict[str, int] | None = None) -> "AdminCatalogFacade":
        repository = InMemoryCatalogRepository()
        category = Category.create(name="Electronics", slug="electronics")
        repository.save_category(category)
        repository.save_product(
            Product.create(
                name="Wireless Headphones",
                slug="wireless-headphones",
                description="Noise cancelling bluetooth headphones",
                price=79.99,
                category_id=category.id,
                stock_quantity=25,
                image_url="https://example.com/headphones.jpg",
            )
        )
        return cls(repository, pending_orders_by_slug=pending_orders_by_slug)

    def _pending_order_count(self, slug: str) -> int:
        return self.pending_orders_by_slug.get(slug, 0)

    def create_category(self, name: str, slug: str, description: str | None = None, parent_slug: str | None = None):
        category = self.manage_category_uc.create(name=name, slug=slug, description=description, parent_slug=parent_slug)
        return {"status": 201, "data": serialize_category(category)}

    def create_product(
        self,
        name: str,
        slug: str,
        description: str,
        price: float,
        category_slug: str,
        stock_quantity: int,
        image_url: str | None = None,
    ):
        product = self.create_product_uc.execute(
            name=name,
            slug=slug,
            description=description,
            price=price,
            category_slug=category_slug,
            stock_quantity=stock_quantity,
            image_url=image_url,
        )
        return {"status": 201, "data": serialize_product(product)}

    def update_product(self, slug: str, **fields):
        product = self.update_product_uc.execute(slug, **fields)
        return {"status": 200, "data": serialize_product(product)}

    def delete_product(self, slug: str):
        try:
            self.delete_product_uc.execute(slug)
            return {"status": 200, "data": {"deleted": True}}
        except PermissionError:
            return {
                "status": 409,
                "error": {
                    "code": "PRODUCT_HAS_PENDING_ORDERS",
                    "message": "Cannot delete product with pending orders",
                },
            }
