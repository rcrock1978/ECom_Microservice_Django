from rewards.domain.entities import RewardAccount


class GetSummaryUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str) -> RewardAccount:
        account = self.repository.get_by_user_id(user_id)
        if not account:
            account = RewardAccount.create(user_id=user_id)
            self.repository.save(account)
        return account
