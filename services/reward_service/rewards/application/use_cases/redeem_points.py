from rewards.domain.entities import RewardAccount


class RedeemPointsUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str, points: int, reason: str):
        account = self.repository.get_by_user_id(user_id)
        if not account:
            account = RewardAccount.create(user_id=user_id)
        account.redeem(points=points, reason=reason)
        return self.repository.save(account)
