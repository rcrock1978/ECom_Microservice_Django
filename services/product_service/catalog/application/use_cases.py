from __future__ import annotations
from typing import List, Optional

from services.product_service.catalog.domain.entities import (
    Product,
    Category,
    filter_products as domain_filter,
    search_products as domain_search,
)


def list_products(products: List[Product], keyword: Optional[str] = None, category: Optional[Category] = None) -> List[Product]:
    return domain_filter(products, keyword=keyword, category=category)


def search_products(products: List[Product], query: str) -> List[Product]:
    return domain_search(products, query)


def get_product_by_slug(products: List[Product], slug: str) -> Product:
    for p in products:
        if p.slug == slug:
            return p
    raise ValueError("Product not found")


def list_categories_tree(categories: List[Category]) -> List[Category]:
    # only return root categories (no parent)
    return [c for c in categories if c.parent is None]
