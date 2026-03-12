from emails.infrastructure.event_consumers import AuthEventConsumer, EmailEventConsumer, OrderEventConsumer
from emails.presentation.views import EmailAdminFacade


def test_event_consumers_render_templates_and_send() -> None:
    auth_consumer = AuthEventConsumer()
    auth_consumer.handle_user_registered({"email": "ray@example.com", "name": "Ray"})

    order_consumer = OrderEventConsumer()
    order_consumer.handle_order_confirmed({"email": "ray@example.com", "order_number": "ORD-7"})

    assert len(auth_consumer.sent_emails) == 1
    assert "Ray" in auth_consumer.sent_emails[0]["body"]
    assert "ORD-7" in order_consumer.sent_emails[0]["body"]


def test_admin_monitoring_endpoints_and_replay() -> None:
    consumer = EmailEventConsumer.in_memory()
    consumer.handle_event("order.confirmed", {"email": "ray@example.com", "order_number": "ORD-9"})

    admin = EmailAdminFacade(consumer.repository)
    overview = admin.get_overview()
    failed_before = admin.list_failed_emails()
    replay = admin.replay_failed()
    failed_after = admin.list_failed_emails()

    assert overview["status"] == 200
    assert overview["data"]["total_messages"] >= 1
    assert failed_before["status"] == 200
    assert replay["status"] == 200
    assert failed_after["status"] == 200
