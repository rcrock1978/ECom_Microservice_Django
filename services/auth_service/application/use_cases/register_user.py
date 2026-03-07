from django.core.mail import send_mail

from ..crypto import hash_password
from ...infrastructure.repositories import UserRepository
from services.auth_service.auth_service.models import UserRole
from shared.message_bus import InMemoryMessageBus


class RegistrationError(Exception):
    pass


def register_user(email: str, password: str, role: UserRole = UserRole.CUSTOMER,
                  user_repo: UserRepository | None = None,
                  bus: InMemoryMessageBus | None = None) -> dict:
    repo = user_repo or UserRepository()
    if repo.get_by_email(email):
        raise RegistrationError("User already exists")
    hashed = hash_password(password)
    user = repo.create(email=email, hashed_password=hashed, role=role)

    # generate verification token
    from .verify_email import generate_verification
    token = generate_verification(user, repo)

    # send confirmation email with token link
    send_mail(
        "Verify your Mango account",
        f"Click here to verify: https://example.com/verify/{token}",
        "no-reply@mango.local",
        [email],
        fail_silently=True,
    )

    # publish event
    if bus:
        bus.publish("user.registered", {"user_id": user.id, "email": user.email})
    return {"id": user.id, "email": user.email, "role": user.role}
