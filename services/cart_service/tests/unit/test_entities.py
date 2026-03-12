from cart.domain.entities import Cart


def test_cart_add_item_updates_subtotal_and_count() -> None:
    cart = Cart.create(user_id="user-1")
    cart.add_item(product_id="p1", product_name="Wireless Headphones", product_price=79.99, quantity=2)

    assert cart.item_count == 2
    assert round(cart.subtotal, 2) == 159.98


def test_cart_update_item_quantity_changes_subtotal() -> None:
    cart = Cart.create(user_id="user-1")
    item = cart.add_item(product_id="p1", product_name="Wireless Headphones", product_price=50.0, quantity=1)

    cart.update_item(item.id, 3)

    assert cart.item_count == 3
    assert round(cart.subtotal, 2) == 150.0
