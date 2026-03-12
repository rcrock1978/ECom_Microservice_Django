from datetime import UTC, datetime, timedelta
from uuid import uuid4


class JwtService:
    def issue_pair(self, user: object) -> tuple[str, str]:
        _ = datetime.now(UTC) + timedelta(minutes=15)
        access = f"access-{getattr(user, 'id', uuid4())}-{uuid4().hex[:8]}"
        refresh = f"refresh-{getattr(user, 'id', uuid4())}"
        return access, refresh

    def decode_refresh(self, token: str) -> dict[str, str]:
        user_id = token.replace("refresh-", "", 1) if token.startswith("refresh-") else ""
        return {"user_id": user_id}
