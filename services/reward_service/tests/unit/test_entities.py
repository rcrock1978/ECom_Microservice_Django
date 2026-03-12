from rewards.domain.entities import RewardAccount, RewardTransaction


def test_reward_account_credit_and_redeem_points() -> None:
    account = RewardAccount.create(user_id="user-1")
    account.credit(points=50, reason="order-confirmed")

    redeemed = account.redeem(points=20, reason="checkout-redemption")

    assert redeemed == 20
    assert account.available_points == 30


def test_reward_transaction_creation_shape() -> None:
    tx = RewardTransaction.create(user_id="user-1", points=15, transaction_type="credit", reason="order")

    assert tx.user_id == "user-1"
    assert tx.points == 15
    assert tx.transaction_type == "credit"
