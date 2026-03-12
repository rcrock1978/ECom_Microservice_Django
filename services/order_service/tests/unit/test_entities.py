from orders.domain.entities import Order, OrderItem


def test_order_total_applies_discount() -> None:
    item = OrderItem.create(product_id="p1", product_name="Headphones", unit_price=100, quantity=2)
    order = Order.create(user_id="user-1", items=[item], discount_amount=15)

    assert order.subtotal == 200
    assert order.total_amount == 185


def test_order_cancel_changes_status() -> None:
    item = OrderItem.create(product_id="p1", product_name="Headphones", unit_price=100, quantity=1)
    order = Order.create(user_id="user-1", items=[item])

    order.cancel()

    assert order.status == "cancelled"
