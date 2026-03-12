from emails.infrastructure.event_consumers import AuthEventConsumer


def test_user_registered_event_is_consumed_once() -> None:
    consumer = AuthEventConsumer()
    consumer.handle_user_registered({"email": "ray@example.com", "name": "Ray"})

    assert len(consumer.sent_emails) == 1
    assert consumer.sent_emails[0]["subject"] == "Welcome to Mango"


def test_password_reset_event_is_consumed() -> None:
    consumer = AuthEventConsumer()
    consumer.handle_password_reset_requested(
        {"email": "ray@example.com", "reset_link": "https://mango.example.com/reset-password?token=abc"}
    )

    assert len(consumer.sent_emails) == 1
    assert "reset-password" in consumer.sent_emails[0]["body"]
