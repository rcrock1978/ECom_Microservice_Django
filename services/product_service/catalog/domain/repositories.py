from abc import ABC, abstractmethod

from catalog.domain.entities import Category, Product


class ProductRepository(ABC):
    @abstractmethod
    def list_products(self, in_stock: bool | None = None) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    def search_products(self, query: str) -> list[Product]:
        raise NotImplementedError

    @abstractmethod
    def get_product_by_slug(self, slug: str) -> Product | None:
        raise NotImplementedError


class CategoryRepository(ABC):
    @abstractmethod
    def list_categories(self) -> list[Category]:
        raise NotImplementedError
