from gateway.infrastructure.jwt_validator import JwtValidator


validator = JwtValidator()


def validate_access_token(access_token: str | None) -> dict[str, object]:
    return validator.validate(access_token)
