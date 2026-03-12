from uuid import uuid4


class ForgotPasswordUseCase:
    def __init__(self, repository: object, event_publisher: object | None = None) -> None:
        self.repository = repository
        self.event_publisher = event_publisher

    def execute(self, email: str) -> dict[str, object]:
        user = self.repository.get_user_by_email(email)
        if not user:
            return {"status": 200}

        token = uuid4().hex
        self.repository.save_reset_token(email, token)
        if self.event_publisher:
            reset_link = f"https://mango.example.com/reset-password?token={token}"
            self.event_publisher.password_reset_requested(user.id, user.email, reset_link)
        return {"status": 200}
