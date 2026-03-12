from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from uuid import uuid4


@dataclass
class User:
    id: str
    name: str
    email: str
    password_hash: str
    role: str = "customer"
    is_active: bool = True
    is_email_verified: bool = False
    failed_login_attempts: int = 0
    locked_until: datetime | None = None

    @classmethod
    def create(cls, name: str, email: str, password_hash: str, role: str = "customer") -> "User":
        return cls(id=str(uuid4()), name=name, email=email.lower(), password_hash=password_hash, role=role)

    def register_failed_login(self, now: datetime | None = None) -> None:
        current_time = now or datetime.now(UTC)
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_until = current_time + timedelta(minutes=15)

    def register_successful_login(self) -> None:
        self.failed_login_attempts = 0
        self.locked_until = None


@dataclass
class RefreshToken:
    id: str
    user_id: str
    token_hash: str
    is_blacklisted: bool = False

    @classmethod
    def create(cls, user_id: str, token_hash: str) -> "RefreshToken":
        return cls(id=str(uuid4()), user_id=user_id, token_hash=token_hash)
