from gateway.infrastructure.jwt_validator import JwtValidator


def test_validator_rejects_invalid_token() -> None:
    validator = JwtValidator()
    result = validator.validate("invalid-token")
    assert result["is_valid"] is False


def test_validator_accepts_stub_access_token_shape() -> None:
    validator = JwtValidator()
    result = validator.validate("access-user-123-admin")
    assert result["is_valid"] is True
    assert result["claims"]["user_id"] == "user"
