class ListTransactionsUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str):
        account = self.repository.get_by_user_id(user_id)
        if not account:
            return []
        return account.transactions
