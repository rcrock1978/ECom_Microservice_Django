from auth.application.crypto import PasswordHasher
from auth.application.jwt_utils import JwtService
from auth.application.use_cases.forgot_password import ForgotPasswordUseCase
from auth.application.use_cases.get_profile import GetProfileUseCase
from auth.application.use_cases.login_user import LoginUserUseCase
from auth.application.use_cases.logout_user import LogoutUserUseCase
from auth.application.use_cases.refresh_token import RefreshTokenUseCase
from auth.application.use_cases.register_user import RegisterUserUseCase
from auth.application.use_cases.reset_password import ResetPasswordUseCase
from auth.infrastructure.event_publisher import AuthEventPublisher
from auth.infrastructure.repositories import InMemoryAuthRepository
from auth.presentation.serializers import serialize_user


class AuthFacade:
    def __init__(self, repository: InMemoryAuthRepository, event_publisher: AuthEventPublisher | None = None) -> None:
        self.repository = repository
        self.event_publisher = event_publisher
        self.jwt_service = JwtService()
        self.hasher = PasswordHasher()
        self.register_user = RegisterUserUseCase(repository, event_publisher)
        self.login_user = LoginUserUseCase(repository, self.hasher, self.jwt_service)
        self.refresh_token = RefreshTokenUseCase(repository, self.jwt_service)
        self.logout_user = LogoutUserUseCase(repository)
        self.get_profile = GetProfileUseCase(repository)
        self.forgot_password_uc = ForgotPasswordUseCase(repository, event_publisher)
        self.reset_password_uc = ResetPasswordUseCase(repository)

    @classmethod
    def in_memory(cls) -> "AuthFacade":
        return cls(InMemoryAuthRepository(), AuthEventPublisher())

    def register(self, name: str, email: str, password: str) -> dict[str, object]:
        user = self.register_user.execute(name=name, email=email, password=password)
        return {"status": 201, "data": serialize_user(user)}

    def login(self, email: str, password: str) -> dict[str, object]:
        payload = self.login_user.execute(email=email, password=password)
        return {
            "status": 200,
            "data": {"user": {"id": payload["user_id"], "email": payload["email"], "name": payload["name"], "role": payload["role"]}},
            "cookies": {"access_token": payload["access_token"], "refresh_token": payload["refresh_token"]},
        }

    def refresh(self, refresh_token: str) -> dict[str, object]:
        payload = self.refresh_token.execute(refresh_token=refresh_token)
        return {"status": 200, "cookies": payload}

    def logout(self, refresh_token: str) -> dict[str, int]:
        self.logout_user.execute(refresh_token=refresh_token)
        return {"status": 204}

    def me(self, email: str) -> dict[str, object]:
        user = self.get_profile.execute(email=email)
        return {"status": 200, "data": serialize_user(user)}

    def forgot_password(self, email: str) -> dict[str, object]:
        result = self.forgot_password_uc.execute(email=email)
        return {"status": result["status"]}

    def reset_password(self, token: str, new_password: str) -> dict[str, object]:
        self.reset_password_uc.execute(token=token, new_password=new_password)
        return {"status": 200}

    def debug_last_reset_token(self, email: str) -> str:
        token = self.repository.get_reset_token(email)
        if not token:
            raise ValueError("No reset token")
        return token
