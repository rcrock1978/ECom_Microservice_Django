from dataclasses import dataclass, field
from datetime import datetime, UTC
from uuid import uuid4


@dataclass
class RewardTransaction:
    id: str
    user_id: str
    points: int
    transaction_type: str
    reason: str
    created_at: datetime

    @classmethod
    def create(cls, user_id: str, points: int, transaction_type: str, reason: str) -> "RewardTransaction":
        return cls(
            id=str(uuid4()),
            user_id=user_id,
            points=points,
            transaction_type=transaction_type,
            reason=reason,
            created_at=datetime.now(UTC),
        )


@dataclass
class RewardAccount:
    id: str
    user_id: str
    available_points: int = 0
    lifetime_earned_points: int = 0
    transactions: list[RewardTransaction] = field(default_factory=list)

    @classmethod
    def create(cls, user_id: str) -> "RewardAccount":
        return cls(id=str(uuid4()), user_id=user_id)

    def credit(self, points: int, reason: str) -> RewardTransaction:
        if points <= 0:
            raise ValueError("Credit points must be positive")
        self.available_points += points
        self.lifetime_earned_points += points
        tx = RewardTransaction.create(
            user_id=self.user_id,
            points=points,
            transaction_type="credit",
            reason=reason,
        )
        self.transactions.append(tx)
        return tx

    def can_redeem(self, points: int) -> bool:
        return points > 0 and self.available_points >= points

    def redeem(self, points: int, reason: str) -> int:
        if not self.can_redeem(points):
            raise ValueError("Insufficient points")
        self.available_points -= points
        tx = RewardTransaction.create(
            user_id=self.user_id,
            points=points,
            transaction_type="redeem",
            reason=reason,
        )
        self.transactions.append(tx)
        return points

    def expire(self, points: int, reason: str) -> int:
        if points <= 0:
            return 0
        expired = min(points, self.available_points)
        self.available_points -= expired
        tx = RewardTransaction.create(
            user_id=self.user_id,
            points=expired,
            transaction_type="expire",
            reason=reason,
        )
        self.transactions.append(tx)
        return expired
