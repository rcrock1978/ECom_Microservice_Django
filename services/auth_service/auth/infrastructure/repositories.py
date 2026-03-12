from dataclasses import dataclass

from auth.domain.entities import RefreshToken, User


@dataclass
class InMemoryAuthRepository:
    users_by_email: dict[str, User] | None = None
    users_by_id: dict[str, User] | None = None
    refresh_tokens: dict[str, RefreshToken] | None = None
    reset_tokens: dict[str, str] | None = None

    def __post_init__(self) -> None:
        self.users_by_email = self.users_by_email or {}
        self.users_by_id = self.users_by_id or {}
        self.refresh_tokens = self.refresh_tokens or {}
        self.reset_tokens = self.reset_tokens or {}

    def save_user(self, user: User) -> User:
        self.users_by_email[user.email] = user
        self.users_by_id[user.id] = user
        return user

    def get_user_by_email(self, email: str) -> User | None:
        return self.users_by_email.get(email.lower())

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.users_by_id.get(user_id)

    def save_refresh_token(self, refresh_token: RefreshToken) -> RefreshToken:
        self.refresh_tokens[refresh_token.token_hash] = refresh_token
        return refresh_token

    def get_refresh_token(self, token_hash: str) -> RefreshToken | None:
        return self.refresh_tokens.get(token_hash)

    def blacklist_refresh_token(self, token_hash: str) -> None:
        token = self.refresh_tokens.get(token_hash)
        if token:
            token.is_blacklisted = True

    def save_reset_token(self, email: str, token: str) -> None:
        self.reset_tokens[email.lower()] = token

    def get_reset_token(self, email: str) -> str | None:
        return self.reset_tokens.get(email.lower())
