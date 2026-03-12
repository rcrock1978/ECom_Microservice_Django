from .factories import user_factory


def make_user_context(role: str = "customer") -> dict[str, str]:
    return user_factory(role=role)
