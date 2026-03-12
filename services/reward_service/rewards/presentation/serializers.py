def serialize_transaction(tx: object) -> dict[str, object]:
    return {
        "id": getattr(tx, "id"),
        "user_id": getattr(tx, "user_id"),
        "points": getattr(tx, "points"),
        "transaction_type": getattr(tx, "transaction_type"),
        "reason": getattr(tx, "reason"),
        "created_at": getattr(tx, "created_at").isoformat(),
    }


def serialize_summary(account: object) -> dict[str, object]:
    return {
        "user_id": getattr(account, "user_id"),
        "available_points": getattr(account, "available_points"),
        "lifetime_earned_points": getattr(account, "lifetime_earned_points"),
    }
