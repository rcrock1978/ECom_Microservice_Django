from orders.infrastructure.service_clients import CartClient, CouponClient, ProductClient, RewardClient


def test_service_clients_contract_shapes() -> None:
    cart = CartClient().get_cart("user-1")
    product = ProductClient().get_product("p1")
    coupon = CouponClient().validate_coupon("SAVE10", 100)
    reward = RewardClient().validate_redemption("user-1", 20)

    assert "items" in cart
    assert product["id"] == "p1"
    assert "discount_amount" in coupon
    assert "is_valid" in reward
