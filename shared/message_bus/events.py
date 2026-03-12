from dataclasses import dataclass, field, asdict
from datetime import datetime, UTC
from typing import Any
from uuid import uuid4


@dataclass(slots=True)
class EventEnvelope:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    version: str = "1.0"
    source: str = ""
    correlation_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class BaseEvent(EventEnvelope):
    pass


@dataclass(slots=True)
class OrderConfirmedEvent(BaseEvent):
    @classmethod
    def create(cls, order_id: str, user_id: str, total: float, correlation_id: str | None = None) -> "OrderConfirmedEvent":
        return cls(
            event_type="order.confirmed",
            source="order-service",
            correlation_id=correlation_id,
            payload={"order_id": order_id, "user_id": user_id, "total": total},
        )


@dataclass(slots=True)
class RewardPointsCreditedEvent(BaseEvent):
    @classmethod
    def create(cls, user_id: str, points: int, order_id: str, correlation_id: str | None = None) -> "RewardPointsCreditedEvent":
        return cls(
            event_type="reward.points_credited",
            source="reward-service",
            correlation_id=correlation_id,
            payload={"user_id": user_id, "points": points, "order_id": order_id},
        )


@dataclass(slots=True)
class InventoryAdjustedEvent(BaseEvent):
    @classmethod
    def create(
        cls,
        product_id: str,
        quantity_delta: int,
        order_id: str,
        correlation_id: str | None = None,
    ) -> "InventoryAdjustedEvent":
        return cls(
            event_type="inventory.adjusted",
            source="product-service",
            correlation_id=correlation_id,
            payload={"product_id": product_id, "quantity_delta": quantity_delta, "order_id": order_id},
        )
