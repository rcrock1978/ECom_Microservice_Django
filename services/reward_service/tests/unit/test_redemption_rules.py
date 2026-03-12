from rewards.domain.entities import RewardAccount


def test_validate_redemption_requires_enough_points() -> None:
    account = RewardAccount.create(user_id="user-1")
    account.credit(points=30, reason="order")

    assert account.can_redeem(20) is True
    assert account.can_redeem(50) is False


def test_cannot_redeem_zero_or_negative_points() -> None:
    account = RewardAccount.create(user_id="user-1")
    account.credit(points=10, reason="order")

    assert account.can_redeem(0) is False
    assert account.can_redeem(-1) is False
