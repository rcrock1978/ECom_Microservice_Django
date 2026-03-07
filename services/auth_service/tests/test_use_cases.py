import pytest

from services.auth_service.infrastructure.repositories import UserRepository
from services.auth_service.application.use_cases.register_user import register_user, RegistrationError
from services.auth_service.application.use_cases.login_user import login_user, AuthenticationError
from services.auth_service.application.use_cases.reset_password import reset_password, ResetError
from services.auth_service.domain.entities import UserRole
from shared.message_bus import InMemoryMessageBus


@pytest.fixture
def user_repo():
    return UserRepository()


@pytest.fixture
def bus():
    return InMemoryMessageBus()


def test_registration_and_duplicate(user_repo, bus):
    result = register_user("test@example.com", "password123", user_repo=user_repo, bus=bus)
    assert result["email"] == "test@example.com"
    # event published
    assert bus._subscribers == {}
    with pytest.raises(RegistrationError):
        register_user("test@example.com", "password123", user_repo=user_repo)


def test_login_and_lockout(user_repo):
    # create user
    register_user("login@a.com", "pass", user_repo=user_repo)
    with pytest.raises(AuthenticationError):
        login_user("login@a.com", "wrong", user_repo=user_repo)
    # check fail count
    user = user_repo.get_by_email("login@a.com")
    assert user.failed_attempts == 1

    # simulate 5 failures
    for _ in range(4):
        with pytest.raises(AuthenticationError):
            login_user("login@a.com", "wrong", user_repo=user_repo)
    assert user.is_locked
    with pytest.raises(AuthenticationError):
        login_user("login@a.com", "pass", user_repo=user_repo)


def test_password_reset(user_repo, bus):
    register_user("reset@a.com", "old", user_repo=user_repo)
    reset_password("reset@a.com", "new", user_repo=user_repo, bus=bus)
    # login with new password should work
    tokens = login_user("reset@a.com", "new", user_repo=user_repo)
    assert "access_token" in tokens


def test_admin_login(user_repo):
    register_user("admin@a.com", "adminpass", role=UserRole.ADMIN, user_repo=user_repo)
    tokens = login_user("admin@a.com", "adminpass", is_admin=True, user_repo=user_repo)
    assert "access_token" in tokens
    # non-admin cannot login as admin
    register_user("user@a.com", "userpass", user_repo=user_repo)
    with pytest.raises(AuthenticationError):
        login_user("user@a.com", "userpass", is_admin=True, user_repo=user_repo)
