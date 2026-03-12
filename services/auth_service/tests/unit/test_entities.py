from datetime import UTC, datetime, timedelta

from auth.domain.entities import User
from auth.domain.value_objects import EmailAddress, PasswordPolicy


def test_email_value_object_normalizes_case() -> None:
    email = EmailAddress("Test.User@Example.COM")
    assert email.value == "test.user@example.com"


def test_password_policy_accepts_strong_password() -> None:
    assert PasswordPolicy.is_valid("StrongPass123") is True


def test_password_policy_rejects_weak_password() -> None:
    assert PasswordPolicy.is_valid("weak") is False


def test_user_lockout_after_five_failures() -> None:
    user = User.create(name="Ray", email="ray@example.com", password_hash="hashed")

    for _ in range(5):
        user.register_failed_login(now=datetime.now(UTC))

    assert user.failed_login_attempts == 5
    assert user.locked_until is not None


def test_user_successful_login_clears_lockout() -> None:
    user = User.create(name="Ray", email="ray@example.com", password_hash="hashed")
    user.failed_login_attempts = 5
    user.locked_until = datetime.now(UTC) + timedelta(minutes=10)

    user.register_successful_login()

    assert user.failed_login_attempts == 0
    assert user.locked_until is None
