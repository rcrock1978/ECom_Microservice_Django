from orders.presentation.views import OrderFacade


def test_create_detail_list_cancel_and_status_update() -> None:
    facade = OrderFacade.in_memory()

    created = facade.create_order(
        user_id="user-1",
        items=[{"product_id": "p1", "product_name": "Headphones", "unit_price": 100, "quantity": 1}],
    )
    assert created["status"] == 201

    order_number = created["data"]["order_number"]
    detail = facade.get_order(order_number)
    assert detail["data"]["order_number"] == order_number

    listing = facade.list_orders("user-1")
    assert len(listing["data"]) == 1

    updated = facade.update_order_status(order_number, "paid")
    assert updated["data"]["status"] == "paid"

    cancelled = facade.cancel_order(order_number)
    assert cancelled["data"]["status"] == "cancelled"


def test_payment_webhook_marks_order_paid() -> None:
    facade = OrderFacade.in_memory()
    created = facade.create_order(
        user_id="user-2",
        items=[{"product_id": "p2", "product_name": "Speaker", "unit_price": 80, "quantity": 1}],
    )

    paid = facade.handle_payment_webhook(created["data"]["order_number"], "success")
    assert paid["data"]["status"] == "paid"
