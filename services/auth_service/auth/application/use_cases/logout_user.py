class LogoutUserUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, refresh_token: str) -> None:
        self.repository.blacklist_refresh_token(refresh_token)
