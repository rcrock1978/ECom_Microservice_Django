from auth.presentation.views import AuthFacade


def test_register_login_and_profile_flow() -> None:
    facade = AuthFacade.in_memory()

    register_result = facade.register(name="Ray", email="ray@example.com", password="StrongPass123")
    assert register_result["data"]["email"] == "ray@example.com"

    login_result = facade.login(email="ray@example.com", password="StrongPass123")
    assert "access_token" in login_result["cookies"]
    assert "refresh_token" in login_result["cookies"]

    profile_result = facade.me(email="ray@example.com")
    assert profile_result["data"]["email"] == "ray@example.com"


def test_refresh_logout_and_password_reset_contracts() -> None:
    facade = AuthFacade.in_memory()
    facade.register(name="Ray", email="ray@example.com", password="StrongPass123")
    login_result = facade.login(email="ray@example.com", password="StrongPass123")

    refresh_result = facade.refresh(login_result["cookies"]["refresh_token"])
    assert "access_token" in refresh_result["cookies"]

    logout_result = facade.logout(login_result["cookies"]["refresh_token"])
    assert logout_result["status"] == 204

    forgot_result = facade.forgot_password(email="ray@example.com")
    assert forgot_result["status"] == 200

    token = facade.debug_last_reset_token("ray@example.com")
    reset_result = facade.reset_password(token=token, new_password="EvenStronger123")
    assert reset_result["status"] == 200
