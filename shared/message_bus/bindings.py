from dataclasses import dataclass


@dataclass(slots=True)
class QueueBinding:
    queue_name: str
    routing_key: str


def default_bindings() -> list[QueueBinding]:
    return [
        QueueBinding(queue_name="orders.confirmed", routing_key="order.confirmed"),
        QueueBinding(queue_name="rewards.credited", routing_key="reward.points_credited"),
        QueueBinding(queue_name="inventory.adjusted", routing_key="inventory.adjusted"),
    ]
