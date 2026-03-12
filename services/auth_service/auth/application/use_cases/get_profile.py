class GetProfileUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository

    def execute(self, email: str) -> object:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ValueError("User not found")
        return user
