from django.core.mail import send_mail

from ..crypto import hash_password
from ...infrastructure.repositories import UserRepository
from shared.message_bus import InMemoryMessageBus


class ResetError(Exception):
    pass


def reset_password(email: str, new_password: str,
                   user_repo: UserRepository | None = None,
                   bus: InMemoryMessageBus | None = None) -> None:
    repo = user_repo or UserRepository()
    user = repo.get_by_email(email)
    if not user:
        raise ResetError("User not found")
    user.hashed_password = hash_password(new_password)
    repo.save(user)
    send_mail(
        "Password Reset",
        "Your password has been changed.",
        "no-reply@mango.local",
        [email],
        fail_silently=True,
    )
    if bus:
        bus.publish("user.password_reset", {"user_id": user.id})
