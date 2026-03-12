from auth.application.use_cases.login_user import LoginUserUseCase
from auth.application.use_cases.refresh_token import RefreshTokenUseCase
from auth.domain.entities import RefreshToken, User
from auth.infrastructure.repositories import InMemoryAuthRepository


class StubHasher:
    def verify(self, plain: str, hashed: str) -> bool:
        return hashed == f"hashed::{plain}"


class StubJwt:
    def issue_pair(self, user: User) -> tuple[str, str]:
        return (f"access-{user.id}", f"refresh-{user.id}")

    def decode_refresh(self, token: str) -> dict[str, str]:
        user_id = token.replace("refresh-", "")
        return {"user_id": user_id}


def test_login_use_case_returns_tokens_for_valid_credentials() -> None:
    repository = InMemoryAuthRepository()
    user = User.create(name="Ray", email="ray@example.com", password_hash="hashed::StrongPass123")
    repository.save_user(user)

    use_case = LoginUserUseCase(repository=repository, hasher=StubHasher(), jwt_service=StubJwt())
    result = use_case.execute(email="ray@example.com", password="StrongPass123")

    assert result["access_token"].startswith("access-")
    assert result["refresh_token"].startswith("refresh-")


def test_refresh_use_case_rotates_refresh_token() -> None:
    repository = InMemoryAuthRepository()
    user = User.create(name="Ray", email="ray@example.com", password_hash="hashed::StrongPass123")
    repository.save_user(user)
    repository.save_refresh_token(RefreshToken.create(user_id=user.id, token_hash=f"refresh-{user.id}"))

    use_case = RefreshTokenUseCase(repository=repository, jwt_service=StubJwt())
    result = use_case.execute(refresh_token=f"refresh-{user.id}")

    assert result["access_token"].startswith("access-")
    assert result["refresh_token"].startswith("refresh-")
