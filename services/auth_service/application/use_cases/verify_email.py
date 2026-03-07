from datetime import timedelta
from django.utils import timezone
import uuid

# use timezone.now() to keep datetimes tz-aware

from ...infrastructure.repositories import UserRepository
from shared.message_bus import InMemoryMessageBus


class VerificationError(Exception):
    pass


def generate_verification(user, repo: UserRepository):
    token = uuid.uuid4().hex
    user.verification_token = token
    # expiration uses timezone-aware now
    user.token_expiry = timezone.now() + timedelta(hours=24)
    repo.save(user)
    return token


def verify_token(token: str, repo: UserRepository | None = None, bus: InMemoryMessageBus | None = None):
    # bypass repository for lookup by token
    from services.auth_service.auth_service.models import User
    try:
        user = User.objects.get(verification_token=token)
    except User.DoesNotExist:
        raise VerificationError("Invalid token")
    if user.token_expiry and timezone.now() > user.token_expiry:
        raise VerificationError("Token expired")
    user.is_verified = True
    user.verification_token = None
    user.token_expiry = None
    repo.save(user)
    if bus:
        bus.publish("user.verified", {"user_id": user.id})
    return True
