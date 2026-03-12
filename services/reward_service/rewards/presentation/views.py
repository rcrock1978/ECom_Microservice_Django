from rewards.application.use_cases.credit_points import CreditPointsUseCase
from rewards.application.use_cases.expire_points import ExpirePointsUseCase
from rewards.application.use_cases.get_summary import GetSummaryUseCase
from rewards.application.use_cases.list_transactions import ListTransactionsUseCase
from rewards.application.use_cases.redeem_points import RedeemPointsUseCase
from rewards.application.use_cases.validate_redemption import ValidateRedemptionUseCase
from rewards.infrastructure.event_publisher import RewardEventPublisher
from rewards.infrastructure.repositories import InMemoryRewardRepository
from rewards.presentation.serializers import serialize_summary, serialize_transaction


class RewardFacade:
    def __init__(self, repository: InMemoryRewardRepository) -> None:
        self.repository = repository
        self.event_publisher = RewardEventPublisher()
        self.get_summary_uc = GetSummaryUseCase(repository)
        self.list_transactions_uc = ListTransactionsUseCase(repository)
        self.validate_redemption_uc = ValidateRedemptionUseCase(repository)
        self.redeem_points_uc = RedeemPointsUseCase(repository)
        self.credit_points_uc = CreditPointsUseCase(repository, self.event_publisher)
        self.expire_points_uc = ExpirePointsUseCase(repository)

    @classmethod
    def in_memory(cls) -> "RewardFacade":
        return cls(InMemoryRewardRepository())

    def get_summary(self, user_id: str) -> dict[str, object]:
        account = self.get_summary_uc.execute(user_id=user_id)
        return {"status": 200, "data": serialize_summary(account)}

    def list_transactions(self, user_id: str) -> dict[str, object]:
        transactions = self.list_transactions_uc.execute(user_id=user_id)
        return {"status": 200, "data": [serialize_transaction(tx) for tx in transactions]}

    def validate_redemption(self, user_id: str, points: int) -> dict[str, object]:
        result = self.validate_redemption_uc.execute(user_id=user_id, points=points)
        return {"status": 200, "data": result}

    def redeem_points(self, user_id: str, points: int, reason: str) -> dict[str, object]:
        account = self.redeem_points_uc.execute(user_id=user_id, points=points, reason=reason)
        return {"status": 200, "data": serialize_summary(account)}

    def credit_points(self, user_id: str, points: int, reason: str) -> dict[str, object]:
        account = self.credit_points_uc.execute(user_id=user_id, points=points, reason=reason)
        return {"status": 200, "data": serialize_summary(account)}

    def expire_points(self, user_id: str, points: int, reason: str) -> dict[str, object]:
        account = self.expire_points_uc.execute(user_id=user_id, points=points, reason=reason)
        if not account:
            return {"status": 404, "data": {"message": "Account not found"}}
        return {"status": 200, "data": serialize_summary(account)}

    def consume_order_confirmed(self, payload: dict[str, object]) -> dict[str, object]:
        user_id = str(payload.get("user_id", ""))
        total_amount = float(payload.get("total_amount", 0))
        points = int(total_amount // 10)
        return self.credit_points(user_id=user_id, points=points, reason="order-confirmed")
