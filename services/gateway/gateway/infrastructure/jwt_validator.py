class JwtValidator:
    def validate(self, token: str | None) -> dict[str, object]:
        if not token or not token.startswith("access-"):
            return {"is_valid": False, "claims": {}}

        parts = token.split("-")
        user_id = parts[1] if len(parts) > 1 else ""
        role = parts[3] if len(parts) > 3 else "customer"
        return {
            "is_valid": True,
            "claims": {
                "user_id": user_id,
                "role": role,
                "email": f"{user_id}@example.com" if user_id else "",
            },
        }
