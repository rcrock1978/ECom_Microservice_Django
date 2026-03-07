from __future__ import annotations
from datetime import timedelta
from typing import Optional
import uuid

from django.utils import timezone

from services.auth_service.auth_service.models import User, RefreshToken
from services.auth_service.auth_service.models import UserRole


class UserRepository:
    """Repository backed by Django ORM."""

    def create(self, email: str, hashed_password: str, role: UserRole = UserRole.CUSTOMER) -> User:
        return User.objects.create(email=email, hashed_password=hashed_password, role=role)

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None

    def save(self, user: User) -> None:
        user.save()

    def lock_user(self, user: User) -> None:
        user.is_locked = True
        user.save()

    def increment_failed_attempts(self, user: User) -> None:
        user.failed_attempts += 1
        if user.failed_attempts >= 5:
            user.is_locked = True
        user.save()

    def reset_failed_attempts(self, user: User) -> None:
        user.failed_attempts = 0
        user.save()


class RefreshTokenRepository:
    def create(self, user_id: int, expires_delta: timedelta = timedelta(days=7)) -> RefreshToken:
        token_str = str(uuid.uuid4())
        expires_at = timezone.now() + expires_delta
        user = User.objects.get(id=user_id)
        return RefreshToken.objects.create(user=user, token=token_str, expires_at=expires_at)

    def get(self, token_str: str) -> Optional[RefreshToken]:
        try:
            return RefreshToken.objects.get(token=token_str)
        except RefreshToken.DoesNotExist:
            return None

    def revoke(self, token: RefreshToken) -> None:
        token.delete()
