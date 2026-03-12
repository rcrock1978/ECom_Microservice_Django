from dataclasses import dataclass
from datetime import datetime, UTC
from uuid import uuid4


@dataclass
class EmailMessage:
    id: str
    to_email: str
    subject: str
    body_text: str
    body_html: str
    event_type: str
    status: str
    retry_count: int
    created_at: datetime

    @classmethod
    def create(
        cls,
        to_email: str,
        subject: str,
        body_text: str,
        body_html: str,
        event_type: str,
    ) -> "EmailMessage":
        return cls(
            id=str(uuid4()),
            to_email=to_email,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            event_type=event_type,
            status="pending",
            retry_count=0,
            created_at=datetime.now(UTC),
        )

    def mark_sent(self) -> None:
        self.status = "sent"

    def mark_failed(self) -> None:
        self.status = "failed"

    def increment_retry(self) -> None:
        self.retry_count += 1
