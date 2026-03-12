from rewards.domain.entities import RewardAccount


class CreditPointsUseCase:
    def __init__(self, repository: object, event_publisher: object | None = None) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, user_id: str, points: int, reason: str):
        account = self.repository.get_by_user_id(user_id)
        if not account:
            account = RewardAccount.create(user_id=user_id)
        account.credit(points=points, reason=reason)
        saved = self.repository.save(account)
        if self.event_publisher:
            self.event_publisher.publish_points_earned(saved.user_id, points)
        return saved
