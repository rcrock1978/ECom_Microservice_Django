from catalog.presentation.views import CatalogFacade


def test_catalog_listing_and_search_contract() -> None:
    facade = CatalogFacade.in_memory_seeded()

    listing = facade.list_products()
    assert listing["status"] == 200
    assert len(listing["data"]) >= 1

    search = facade.search_products("wireless")
    assert search["status"] == 200
    assert any("wireless" in item["slug"] for item in search["data"])


def test_product_detail_and_category_tree_contract() -> None:
    facade = CatalogFacade.in_memory_seeded()

    detail = facade.get_product_detail("wireless-headphones")
    assert detail["status"] == 200
    assert detail["data"]["slug"] == "wireless-headphones"

    categories = facade.list_categories()
    assert categories["status"] == 200
    assert len(categories["data"]) >= 1
