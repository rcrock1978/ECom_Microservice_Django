from orders.domain.entities import Order, OrderItem


def test_order_status_transition_from_pending_to_paid() -> None:
    item = OrderItem.create(product_id="p1", product_name="Headphones", unit_price=80, quantity=1)
    order = Order.create(user_id="user-1", items=[item])

    order.mark_paid()

    assert order.status == "paid"


def test_order_cannot_ship_before_paid() -> None:
    item = OrderItem.create(product_id="p1", product_name="Headphones", unit_price=80, quantity=1)
    order = Order.create(user_id="user-1", items=[item])

    try:
        order.mark_shipped()
    except ValueError as error:
        assert "paid" in str(error)
    else:
        raise AssertionError("Expected ValueError")
