import pytest

from services.product_service.catalog.domain.entities import Product, Category

# these functions will be implemented in application layer
from services.product_service.catalog.application.use_cases import (
    list_products,
    search_products as search_products_uc,
    get_product_by_slug,
    list_categories_tree,
)


def test_list_products_filters():
    cat = Category(id=1, name="Cat")
    p1 = Product(id=1, name="Apple", slug="apple", description="", price=1.0, category=cat)
    p2 = Product(id=2, name="Banana", slug="banana", description="", price=1.0, category=None)
    result = list_products([p1, p2], keyword="app")
    assert result == [p1]
    result = list_products([p1, p2], category=cat)
    assert result == [p1]


def test_search_products_fulltext():
    p1 = Product(id=1, name="Red shirt", slug="red-shirt", description="A red shirt", price=10, category=None)
    p2 = Product(id=2, name="Blue jeans", slug="blue-jeans", description="Denim", price=20, category=None)
    result = search_products_uc([p1, p2], "red")
    assert result == [p1]


def test_get_product_by_slug():
    p1 = Product(id=1, name="Apple", slug="apple", description="", price=1, category=None)
    p2 = Product(id=2, name="Banana", slug="banana", description="", price=1, category=None)
    products = [p1, p2]
    assert get_product_by_slug(products, "apple") == p1
    with pytest.raises(Exception):
        get_product_by_slug(products, "none")


def test_list_categories_tree():
    root = Category(id=1, name="Root")
    child = Category(id=2, name="Child", parent=root)
    root.children = [child]
    # list_categories_tree should return only root nodes
    assert list_categories_tree([root, child]) == [root]
