from datetime import timedelta
from typing import Optional

from ..crypto import verify_password
from ..jwt_utils import create_access_token
from ...infrastructure.repositories import UserRepository, RefreshTokenRepository
from services.auth_service.auth_service.models import UserRole
from shared.message_bus import InMemoryMessageBus


class AuthenticationError(Exception):
    pass


def login_user(email: str, password: str, is_admin: bool = False,
               user_repo: UserRepository | None = None,
               token_repo: RefreshTokenRepository | None = None,
               bus: InMemoryMessageBus | None = None) -> dict:
    repo = user_repo or UserRepository()
    token_repo = token_repo or RefreshTokenRepository()

    user = repo.get_by_email(email)
    if not user:
        raise AuthenticationError("Invalid credentials")
    if user.is_locked:
        raise AuthenticationError("Account locked")
    if not user.is_verified:
        raise AuthenticationError("Email not verified")
    if not verify_password(password, user.hashed_password):
        repo.increment_failed_attempts(user)
        raise AuthenticationError("Invalid credentials")

    repo.reset_failed_attempts(user)
    if is_admin and user.role != UserRole.ADMIN:
        raise AuthenticationError("Admin privileges required")

    access = create_access_token({"user_id": user.id, "role": user.role}, expires_delta=timedelta(minutes=60))
    refresh = token_repo.create(user_id=user.id)
    # publish login event
    if bus:
        bus.publish("user.logged_in", {"user_id": user.id})

    return {"access_token": access, "refresh_token": refresh.token}
