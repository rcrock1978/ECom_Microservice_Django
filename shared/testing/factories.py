from uuid import uuid4


def user_factory(role: str = "customer") -> dict[str, str]:
    return {
        "id": str(uuid4()),
        "email": f"user-{uuid4().hex[:8]}@example.com",
        "role": role,
    }
