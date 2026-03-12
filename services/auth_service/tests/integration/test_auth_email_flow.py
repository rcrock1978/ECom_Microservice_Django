from auth.presentation.views import AuthFacade
from emails.infrastructure.event_consumers import AuthEventConsumer


def test_registration_event_drives_welcome_email() -> None:
    facade = AuthFacade.in_memory()
    consumer = AuthEventConsumer()

    result = facade.register(name="Ray", email="ray@example.com", password="StrongPass123")
    payload = {"email": result["data"]["email"], "name": result["data"]["name"]}
    consumer.handle_user_registered(payload)

    assert len(consumer.sent_emails) == 1
    assert consumer.sent_emails[0]["to"] == "ray@example.com"


def test_forgot_password_event_drives_reset_email() -> None:
    facade = AuthFacade.in_memory()
    consumer = AuthEventConsumer()

    facade.register(name="Ray", email="ray@example.com", password="StrongPass123")
    facade.forgot_password(email="ray@example.com")

    token = facade.debug_last_reset_token("ray@example.com")
    consumer.handle_password_reset_requested(
        {
            "email": "ray@example.com",
            "reset_link": f"https://mango.example.com/reset-password?token={token}",
        }
    )

    assert len(consumer.sent_emails) == 1
    assert "reset-password" in consumer.sent_emails[0]["body"]
