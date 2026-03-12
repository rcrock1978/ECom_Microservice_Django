from catalog.domain.entities import Product
from catalog.infrastructure.repositories import InMemoryCatalogRepository


def test_search_matches_name_or_description() -> None:
    repository = InMemoryCatalogRepository()
    repository.save_product(
        Product.create(
            name="Wireless Headphones",
            slug="wireless-headphones",
            description="Noise cancelling bluetooth",
            price=79.99,
            category_id="cat-1",
            stock_quantity=10,
        )
    )
    repository.save_product(
        Product.create(
            name="Coffee Mug",
            slug="coffee-mug",
            description="Ceramic mug",
            price=12.99,
            category_id="cat-2",
            stock_quantity=10,
        )
    )

    results = repository.search_products("wireless")
    assert len(results) == 1
    assert results[0].slug == "wireless-headphones"


def test_filter_in_stock_only() -> None:
    repository = InMemoryCatalogRepository()
    repository.save_product(
        Product.create(
            name="In Stock",
            slug="in-stock",
            description="Ready",
            price=10.0,
            category_id="cat-1",
            stock_quantity=5,
        )
    )
    repository.save_product(
        Product.create(
            name="Out Stock",
            slug="out-stock",
            description="None",
            price=11.0,
            category_id="cat-1",
            stock_quantity=0,
        )
    )

    results = repository.list_products(in_stock=True)
    assert len(results) == 1
    assert results[0].slug == "in-stock"
