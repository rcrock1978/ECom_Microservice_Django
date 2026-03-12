from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class BaseEntity:
    id: int


@dataclass
class Category(BaseEntity):
    name: str
    parent: Optional[Category] = None
    children: List[Category] = field(default_factory=list)

    def add_child(self, child: Category):
        child.parent = self
        self.children.append(child)


@dataclass
class Product(BaseEntity):
    name: str
    slug: str
    description: str
    price: float
    category: Optional[Category] = None


# domain logic helpers

def filter_products(products: List[Product], keyword: Optional[str] = None, category: Optional[Category] = None) -> List[Product]:
    result = products
    if keyword:
        lower = keyword.lower()
        result = [p for p in result if lower in p.name.lower() or lower in p.description.lower()]
    if category:
        result = [p for p in result if p.category == category]
    return result


def search_products(products: List[Product], query: str) -> List[Product]:
    return filter_products(products, keyword=query)
