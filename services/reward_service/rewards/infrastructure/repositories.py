from rewards.domain.entities import RewardAccount


class InMemoryRewardRepository:
    def __init__(self) -> None:
        self._accounts: dict[str, RewardAccount] = {}

    def get_by_user_id(self, user_id: str) -> RewardAccount | None:
        return self._accounts.get(user_id)

    def save(self, account: RewardAccount) -> RewardAccount:
        self._accounts[account.user_id] = account
        return account

    def list_accounts(self) -> list[RewardAccount]:
        return list(self._accounts.values())
