from datetime import UTC, datetime

from auth.domain.entities import RefreshToken


class LoginUserUseCase:
    def __init__(self, repository: object, hasher: object, jwt_service: object) -> None:
        self.repository = repository
        self.hasher = hasher
        self.jwt_service = jwt_service

    def execute(self, email: str, password: str) -> dict[str, str]:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")

        if user.locked_until and user.locked_until > datetime.now(UTC):
            raise PermissionError("Account locked")

        if not self.hasher.verify(password, user.password_hash):
            user.register_failed_login()
            self.repository.save_user(user)
            raise ValueError("Invalid credentials")

        user.register_successful_login()
        self.repository.save_user(user)
        access_token, refresh_token = self.jwt_service.issue_pair(user)
        self.repository.save_refresh_token(RefreshToken.create(user_id=user.id, token_hash=refresh_token))

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "role": user.role,
        }
