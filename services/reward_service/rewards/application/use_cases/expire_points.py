class ExpirePointsUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str, points: int, reason: str):
        account = self.repository.get_by_user_id(user_id)
        if not account:
            return None
        account.expire(points=points, reason=reason)
        return self.repository.save(account)

    def execute_scheduled(self, points: int, reason: str) -> int:
        expired_accounts = 0
        for account in self.repository.list_accounts():
            before = account.available_points
            account.expire(points=points, reason=reason)
            self.repository.save(account)
            if account.available_points != before:
                expired_accounts += 1
        return expired_accounts
