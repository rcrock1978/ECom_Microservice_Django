from shared.message_bus.events import EventEnvelope
from shared.message_bus.publisher import MessagePublisher


class AuthEventPublisher:
    def __init__(self) -> None:
        self.publisher = MessagePublisher()

    def user_registered(self, user_id: str, email: str, name: str) -> dict[str, str]:
        event = EventEnvelope(
            event_type="auth.user.registered",
            source="auth-service",
            payload={"user_id": user_id, "email": email, "name": name},
        )
        return self.publisher.publish(event, routing_key="auth.user.registered")

    def password_reset_requested(self, user_id: str, email: str, reset_link: str) -> dict[str, str]:
        event = EventEnvelope(
            event_type="auth.user.password_reset_requested",
            source="auth-service",
            payload={"user_id": user_id, "email": email, "reset_link": reset_link},
        )
        return self.publisher.publish(event, routing_key="auth.user.password_reset_requested")
