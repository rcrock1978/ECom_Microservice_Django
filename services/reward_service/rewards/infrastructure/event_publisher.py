from shared.message_bus.events import RewardPointsCreditedEvent
from shared.message_bus.publisher import MessagePublisher


class RewardEventPublisher:
    def __init__(self, publisher: MessagePublisher | None = None) -> None:
        self.publisher = publisher or MessagePublisher()
        self.published: list[dict[str, object]] = []

    def publish_points_earned(self, user_id: str, points: int) -> None:
        event = RewardPointsCreditedEvent.create(user_id=user_id, points=points, order_id="")
        self.publisher.publish(event=event, routing_key="reward.points_credited")
        self.published.append({"user_id": user_id, "points": points})
