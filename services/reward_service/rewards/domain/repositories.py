from typing import Protocol

from rewards.domain.entities import RewardAccount


class RewardRepository(Protocol):
    def get_by_user_id(self, user_id: str) -> RewardAccount | None: ...

    def save(self, account: RewardAccount) -> RewardAccount: ...

    def list_accounts(self) -> list[RewardAccount]: ...
