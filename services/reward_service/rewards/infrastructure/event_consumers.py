from rewards.application.use_cases.credit_points import CreditPointsUseCase
from rewards.application.use_cases.redeem_points import RedeemPointsUseCase
from rewards.infrastructure.event_publisher import RewardEventPublisher
from rewards.infrastructure.repositories import InMemoryRewardRepository


class RewardEventConsumer:
    def __init__(
        self,
        repository: InMemoryRewardRepository | None = None,
        event_publisher: RewardEventPublisher | None = None,
    ) -> None:
        self.repository = repository or InMemoryRewardRepository()
        self.event_publisher = event_publisher or RewardEventPublisher()
        self.credit_use_case = CreditPointsUseCase(self.repository, self.event_publisher)
        self.redeem_use_case = RedeemPointsUseCase(self.repository)
        self.transactions: list[dict[str, object]] = []

    def handle_order_confirmed(self, payload: dict[str, object]) -> None:
        total = float(payload.get("total_amount", 0))
        points = int(total // 10)
        user_id = str(payload.get("user_id", ""))
        self.credit_use_case.execute(user_id=user_id, points=points, reason="order-confirmed")
        self.transactions.append(
            {
                "user_id": user_id,
                "order_number": payload.get("order_number"),
                "points": points,
                "type": "credit",
            }
        )

    def handle_reward_redeemed(self, payload: dict[str, object]) -> None:
        user_id = str(payload.get("user_id", ""))
        points = int(payload.get("points", 0))
        self.redeem_use_case.execute(user_id=user_id, points=points, reason="checkout-redemption")
        self.transactions.append(
            {
                "user_id": user_id,
                "order_number": payload.get("order_number"),
                "points": points,
                "type": "redeem",
            }
        )
