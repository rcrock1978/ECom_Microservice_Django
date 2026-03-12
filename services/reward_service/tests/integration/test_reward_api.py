from rewards.presentation.views import RewardFacade


def test_reward_summary_history_and_redemption_flow() -> None:
    facade = RewardFacade.in_memory()

    facade.credit_points(user_id="user-1", points=40, reason="order-confirmed")

    summary = facade.get_summary("user-1")
    assert summary["status"] == 200
    assert summary["data"]["available_points"] == 40

    history = facade.list_transactions("user-1")
    assert history["status"] == 200
    assert len(history["data"]) >= 1

    validation = facade.validate_redemption(user_id="user-1", points=20)
    assert validation["data"]["is_valid"] is True

    redeemed = facade.redeem_points(user_id="user-1", points=20, reason="checkout")
    assert redeemed["status"] == 200
    assert redeemed["data"]["available_points"] == 20


def test_order_confirmed_consumption_and_expire_points() -> None:
    facade = RewardFacade.in_memory()

    consumed = facade.consume_order_confirmed(
        {"user_id": "user-2", "order_number": "ORD-1", "total_amount": "120.00"}
    )
    assert consumed["status"] == 200
    assert consumed["data"]["available_points"] == 12

    expired = facade.expire_points(user_id="user-2", points=2, reason="monthly-expiry")
    assert expired["status"] == 200
    assert expired["data"]["available_points"] == 10
