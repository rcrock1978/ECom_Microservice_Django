from datetime import timedelta

from ..jwt_utils import create_access_token
from ...infrastructure.repositories import RefreshTokenRepository, UserRepository
from shared.message_bus import InMemoryMessageBus


class RefreshError(Exception):
    pass


def refresh_access(refresh_token_str: str,
                   token_repo: RefreshTokenRepository | None = None,
                   user_repo: UserRepository | None = None,
                   bus: InMemoryMessageBus | None = None) -> dict:
    token_repo = token_repo or RefreshTokenRepository()
    user_repo = user_repo or UserRepository()

    token = token_repo.get(refresh_token_str)
    if not token or token.is_expired():
        raise RefreshError("Invalid or expired refresh token")

    user = user_repo.get_by_email(token.user.email) if hasattr(token.user, 'email') else user_repo.get_by_email('')
    # issue new access and rotate refresh
    access = create_access_token({"user_id": token.user.id, "role": token.user.role}, expires_delta=timedelta(minutes=60))
    token_repo.revoke(token)
    new_token = token_repo.create(user_id=token.user.id)
    if bus:
        bus.publish("user.refreshed", {"user_id": token.user.id})
    return {"access_token": access, "refresh_token": new_token.token}
