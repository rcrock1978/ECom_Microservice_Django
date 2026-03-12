from auth.domain.entities import RefreshToken


class RefreshTokenUseCase:
    def __init__(self, repository: object, jwt_service: object) -> None:
        self.repository = repository
        self.jwt_service = jwt_service

    def execute(self, refresh_token: str) -> dict[str, str]:
        stored = self.repository.get_refresh_token(refresh_token)
        if not stored or stored.is_blacklisted:
            raise PermissionError("Invalid refresh token")

        payload = self.jwt_service.decode_refresh(refresh_token)
        user = self.repository.get_user_by_id(payload["user_id"])
        if not user:
            raise PermissionError("Invalid refresh token")

        self.repository.blacklist_refresh_token(refresh_token)
        access_token, new_refresh_token = self.jwt_service.issue_pair(user)
        self.repository.save_refresh_token(RefreshToken.create(user_id=user.id, token_hash=new_refresh_token))

        return {"access_token": access_token, "refresh_token": new_refresh_token}
