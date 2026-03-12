class ListOrdersUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, user_id: str):
        return self.repository.list_by_user_id(user_id)
