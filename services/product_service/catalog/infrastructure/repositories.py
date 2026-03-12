from catalog.domain.entities import Category, Product


class InMemoryCatalogRepository:
    def __init__(self) -> None:
        self.products: list[Product] = []
        self.categories: list[Category] = []
        self._product_cache: dict[tuple[str, bool | None], list[Product]] = {}
        self._search_cache: dict[str, list[Product]] = {}

    def _invalidate_cache(self) -> None:
        self._product_cache.clear()
        self._search_cache.clear()

    def save_product(self, product: Product) -> Product:
        self.products = [item for item in self.products if item.id != product.id]
        self.products.append(product)
        self._invalidate_cache()
        return product

    def save_category(self, category: Category) -> Category:
        self.categories = [item for item in self.categories if item.id != category.id]
        self.categories.append(category)
        self._invalidate_cache()
        return category

    def list_products(self, in_stock: bool | None = None) -> list[Product]:
        cache_key = ("list", in_stock)
        cached = self._product_cache.get(cache_key)
        if cached is not None:
            return list(cached)
        products = [item for item in self.products if item.is_active]
        if in_stock is True:
            products = [item for item in products if item.is_in_stock]
        self._product_cache[cache_key] = list(products)
        return products

    def search_products(self, query: str) -> list[Product]:
        normalized = query.lower().strip()
        cached = self._search_cache.get(normalized)
        if cached is not None:
            return list(cached)
        results = [
            item
            for item in self.products
            if normalized in item.name.lower() or normalized in item.description.lower()
        ]
        self._search_cache[normalized] = list(results)
        return results

    def get_product_by_slug(self, slug: str) -> Product | None:
        for product in self.products:
            if product.slug == slug and product.is_active:
                return product
        return None

    def get_product_by_slug_any_state(self, slug: str) -> Product | None:
        for product in self.products:
            if product.slug == slug:
                return product
        return None

    def get_category_by_slug(self, slug: str) -> Category | None:
        for category in self.categories:
            if category.slug == slug and category.is_active:
                return category
        return None

    def list_categories(self) -> list[Category]:
        return [item for item in self.categories if item.is_active]
