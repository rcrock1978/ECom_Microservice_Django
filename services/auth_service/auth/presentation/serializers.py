def serialize_user(user: object) -> dict[str, str]:
    return {
        "id": getattr(user, "id"),
        "name": getattr(user, "name"),
        "email": getattr(user, "email"),
        "role": getattr(user, "role", "customer"),
    }
