class ListCouponsUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, active_only: bool = False):
        return self.repository.list(active_only=active_only)
