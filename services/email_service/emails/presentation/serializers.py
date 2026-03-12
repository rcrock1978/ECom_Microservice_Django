def serialize_email_message(message: object) -> dict[str, object]:
    return {
        "id": getattr(message, "id"),
        "to_email": getattr(message, "to_email"),
        "subject": getattr(message, "subject"),
        "event_type": getattr(message, "event_type"),
        "status": getattr(message, "status"),
        "retry_count": getattr(message, "retry_count"),
    }
