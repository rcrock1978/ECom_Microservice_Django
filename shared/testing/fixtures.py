from .factories import user_factory


def make_user_context(role: str = "customer") -> dict[str, str]:
    return user_factory(role=role)


def make_event_payload(**fields) -> dict[str, object]:
    return dict(fields)


def replay_dlq_messages(dlq: object, callback) -> int:
    return dlq.replay(callback)


def first_purchase_success_event() -> dict[str, object]:
    return {
        "funnel": "first_purchase",
        "step": "checkout_success",
        "converted": True,
        "order_number": "ORD-FIRST-001",
    }
