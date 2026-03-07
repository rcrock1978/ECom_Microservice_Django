from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class UserRole(str, Enum):
    CUSTOMER = "customer"
    ADMIN = "admin"


@dataclass
class BaseEntity:
    id: int


@dataclass
class User(BaseEntity):
    email: str
    hashed_password: str
    role: UserRole = UserRole.CUSTOMER
    is_locked: bool = False
    failed_attempts: int = 0
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class RefreshToken(BaseEntity):
    user_id: int
    token: str
    expires_at: datetime
