from emails.infrastructure.event_consumers import OrderEventConsumer
from orders.presentation.views import OrderFacade
from rewards.infrastructure.event_consumers import RewardEventConsumer


def test_checkout_confirmation_triggers_reward_and_email_side_effects() -> None:
    facade = OrderFacade.in_memory()
    reward_consumer = RewardEventConsumer()
    email_consumer = OrderEventConsumer()

    created = facade.create_order(
        user_id="user-1",
        items=[{"product_id": "p1", "product_name": "Headphones", "unit_price": 120, "quantity": 1}],
        email="user@example.com",
    )
    order_number = created["data"]["order_number"]

    confirmed = facade.handle_payment_webhook(order_number, "success")
    payload = confirmed["data"]

    reward_consumer.handle_order_confirmed(payload)
    email_consumer.handle_order_confirmed(payload)

    assert reward_consumer.transactions[0]["user_id"] == "user-1"
    assert email_consumer.sent_emails[0]["to"] == "user@example.com"
