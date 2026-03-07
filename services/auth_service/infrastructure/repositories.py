from __future__ import annotations
from typing import Dict, Optional
from datetime import datetime, timedelta
from uuid import uuid4

from ..domain.entities import User, RefreshToken, UserRole


class UserRepository:
    """In-memory user repository for prototype/testing."""

    def __init__(self):
        self._users: Dict[int, User] = {}
        self._by_email: Dict[str, User] = {}
        self._next_id = 1

    def create(self, email: str, hashed_password: str, role: UserRole = UserRole.CUSTOMER) -> User:
        user = User(id=self._next_id, email=email, hashed_password=hashed_password, role=role)
        self._next_id += 1
        self._users[user.id] = user
        self._by_email[email] = user
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self._by_email.get(email)

    def save(self, user: User) -> None:
        user.updated_at = datetime.utcnow()
        self._users[user.id] = user
        self._by_email[user.email] = user

    def lock_user(self, user: User) -> None:
        user.is_locked = True
        self.save(user)

    def increment_failed_attempts(self, user: User) -> None:
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            user.is_locked = True
        self.save(user)

    def reset_failed_attempts(self, user: User) -> None:
        user.failed_attempts = 0
        self.save(user)


class RefreshTokenRepository:
    def __init__(self):
        self._tokens: Dict[int, RefreshToken] = {}
        self._by_token: Dict[str, RefreshToken] = {}
        self._next_id = 1

    def create(self, user_id: int, expires_delta: timedelta = timedelta(days=7)) -> RefreshToken:
        token_str = str(uuid4())
        expires_at = datetime.utcnow() + expires_delta
        token = RefreshToken(id=self._next_id, user_id=user_id, token=token_str, expires_at=expires_at)
        self._next_id += 1
        self._tokens[token.id] = token
        self._by_token[token_str] = token
        return token

    def get(self, token_str: str) -> Optional[RefreshToken]:
        return self._by_token.get(token_str)

    def revoke(self, token: RefreshToken) -> None:
        self._tokens.pop(token.id, None)
        self._by_token.pop(token.token, None)
