import pytest

# we expect domain classes and helper functions to exist
from services.product_service.catalog.domain.entities import (
    Product,
    Category,
    filter_products,
    search_products,
)


def test_product_dataclass():
    cat = Category(id=1, name="Cat", parent=None)
    prod = Product(id=1, name="Widget", slug="widget", description="nice", price=9.99, category=cat)
    assert prod.name == "Widget"
    assert prod.category == cat


def test_category_tree():
    root = Category(id=1, name="Root")
    child = Category(id=2, name="Child", parent=root)
    # emulating back-reference
    root.children = [child]
    assert child.parent == root
    assert root.children[0] == child


def test_filter_products_by_keyword():
    p1 = Product(id=1, name="Apple", slug="apple", description="", price=1.0, category=None)
    p2 = Product(id=2, name="Banana", slug="banana", description="", price=1.0, category=None)
    filtered = filter_products([p1, p2], keyword="App")
    assert filtered == [p1]


def test_search_products_fulltext():
    p1 = Product(id=1, name="Red shirt", slug="red-shirt", description="A red shirt", price=10, category=None)
    p2 = Product(id=2, name="Blue jeans", slug="blue-jeans", description="Denim", price=20, category=None)
    result = search_products([p1, p2], "red")
    assert result == [p1]
