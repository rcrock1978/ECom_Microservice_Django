from cart.presentation.views import CartFacade


def test_cart_add_update_remove_flow() -> None:
    facade = CartFacade.in_memory()
    added = facade.add_item("user-1", "p1", "Headphones", 79.99, 1)
    assert added["status"] == 200

    item_id = added["data"]["items"][0]["id"]
    updated = facade.update_item("user-1", item_id, 2)
    assert updated["data"]["item_count"] == 2

    removed = facade.remove_item("user-1", item_id)
    assert removed["data"]["item_count"] == 0


def test_cart_coupon_apply_and_remove_flow() -> None:
    facade = CartFacade.in_memory()
    facade.add_item("user-1", "p1", "Headphones", 79.99, 1)

    applied = facade.apply_coupon("user-1", "SAVE20")
    assert applied["data"]["coupon_code"] == "SAVE20"

    removed = facade.remove_coupon("user-1")
    assert removed["data"]["coupon_code"] is None
