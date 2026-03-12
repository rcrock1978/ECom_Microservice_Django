from django.http import HttpRequest, HttpResponseNotFound, JsonResponse

from catalog.application.use_cases.get_product_detail import GetProductDetailUseCase
from catalog.application.use_cases.list_categories import ListCategoriesUseCase
from catalog.application.use_cases.list_products import ListProductsUseCase
from catalog.application.use_cases.search_products import SearchProductsUseCase
from catalog.domain.entities import Category, Product
from catalog.infrastructure.repositories import InMemoryCatalogRepository
from catalog.presentation.serializers import serialize_category, serialize_product


class CatalogFacade:
    def __init__(self, repository: InMemoryCatalogRepository) -> None:
        self.repository = repository
        self.list_products_uc = ListProductsUseCase(repository)
        self.search_products_uc = SearchProductsUseCase(repository)
        self.get_product_uc = GetProductDetailUseCase(repository)
        self.list_categories_uc = ListCategoriesUseCase(repository)

    @classmethod
    def in_memory_seeded(cls) -> "CatalogFacade":
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
        repository.save_product(
            Product.create(
                name="Portable Speaker",
                slug="portable-speaker",
                description="Compact speaker",
                price=39.99,
                category_id=category.id,
                stock_quantity=0,
            )
        )
        return cls(repository)

    def list_products(self, in_stock: bool | None = None) -> dict[str, object]:
        products = self.list_products_uc.execute(in_stock=in_stock)
        return {"status": 200, "data": [serialize_product(item) for item in products]}

    def search_products(self, query: str) -> dict[str, object]:
        products = self.search_products_uc.execute(query=query)
        return {"status": 200, "data": [serialize_product(item) for item in products]}

    def get_product_detail(self, slug: str) -> dict[str, object]:
        product = self.get_product_uc.execute(slug=slug)
        return {"status": 200, "data": serialize_product(product)}

    def list_categories(self) -> dict[str, object]:
        categories = self.list_categories_uc.execute()
        return {"status": 200, "data": [serialize_category(item) for item in categories]}


_catalog_facade = CatalogFacade.in_memory_seeded()


def list_products_view(request: HttpRequest) -> JsonResponse:
    query = (request.GET.get("q") or "").strip()
    in_stock_param = request.GET.get("in_stock")
    in_stock: bool | None = None
    if in_stock_param is not None:
        in_stock = in_stock_param.lower() in {"1", "true", "yes"}

    result = _catalog_facade.search_products(query=query) if query else _catalog_facade.list_products(in_stock=in_stock)
    return JsonResponse(result)


def product_detail_view(_: HttpRequest, slug: str) -> JsonResponse:
    try:
        result = _catalog_facade.get_product_detail(slug=slug)
        return JsonResponse(result)
    except ValueError:
        return HttpResponseNotFound('{"detail":"Product not found"}', content_type="application/json")


def list_categories_view(_: HttpRequest) -> JsonResponse:
    result = _catalog_facade.list_categories()
    return JsonResponse(result)


def category_detail_view(_: HttpRequest, slug: str) -> JsonResponse:
    categories = _catalog_facade.list_categories()["data"]
    for category in categories:
        if category.get("slug") == slug:
            return JsonResponse({"status": 200, "data": category})
    return HttpResponseNotFound('{"detail":"Category not found"}', content_type="application/json")
