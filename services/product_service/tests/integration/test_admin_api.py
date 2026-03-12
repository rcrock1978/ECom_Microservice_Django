from catalog.presentation.admin_views import AdminCatalogFacade


def test_admin_product_and_category_management_flow() -> None:
    facade = AdminCatalogFacade.in_memory_seeded()

    created_category = facade.create_category(name="Accessories", slug="accessories")
    assert created_category["status"] == 201

    created_product = facade.create_product(
        name="USB-C Cable",
        slug="usb-c-cable",
        description="Braided cable",
        price=12.99,
        category_slug="accessories",
        stock_quantity=100,
    )
    assert created_product["status"] == 201

    updated_product = facade.update_product("usb-c-cable", price=14.99, stock_quantity=80)
    assert updated_product["status"] == 200
    assert updated_product["data"]["price"] == "14.99"

    deleted = facade.delete_product("usb-c-cable")
    assert deleted["status"] == 200


def test_admin_delete_product_blocked_when_pending_orders_exist() -> None:
    facade = AdminCatalogFacade.in_memory_seeded(
        pending_orders_by_slug={"wireless-headphones": 2}
    )

    blocked = facade.delete_product("wireless-headphones")

    assert blocked["status"] == 409
    assert blocked["error"]["code"] == "PRODUCT_HAS_PENDING_ORDERS"
