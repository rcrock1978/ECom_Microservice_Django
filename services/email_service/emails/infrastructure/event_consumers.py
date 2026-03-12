from pathlib import Path

from emails.application.use_cases.process_event_email import ProcessEventEmailUseCase
from emails.application.use_cases.retry_email import RetryEmailUseCase
from emails.application.use_cases.send_email import SendEmailUseCase
from emails.infrastructure.repositories import InMemoryEmailRepository
from emails.infrastructure.smtp_provider import InMemorySmtpProvider


class AuthEventConsumer:
    def __init__(self) -> None:
        self.sent_emails: list[dict[str, str]] = []

    def _load_template(self, name: str) -> str:
        template_dir = Path(__file__).parent / "templates"
        return (template_dir / name).read_text(encoding="utf-8")

    def handle_user_registered(self, payload: dict[str, str]) -> None:
        template = self._load_template("welcome_email.txt")
        body = template.format(name=payload.get("name", "Customer"))
        self.sent_emails.append({"to": payload["email"], "subject": "Welcome to Mango", "body": body})

    def handle_password_reset_requested(self, payload: dict[str, str]) -> None:
        template = self._load_template("password_reset.txt")
        body = template.format(reset_link=payload.get("reset_link", ""))
        self.sent_emails.append({"to": payload["email"], "subject": "Reset your password", "body": body})


class OrderEventConsumer:
    def __init__(self) -> None:
        self.sent_emails: list[dict[str, str]] = []

    def handle_order_confirmed(self, payload: dict[str, object]) -> None:
        order_number = str(payload.get("order_number", ""))
        body = f"Your order {order_number} is confirmed."
        self.sent_emails.append(
            {
                "to": str(payload.get("email", "")),
                "subject": "Order Confirmation",
                "body": body,
            }
        )


class EmailEventConsumer:
    def __init__(self, repository: InMemoryEmailRepository | None = None, smtp_provider: InMemorySmtpProvider | None = None) -> None:
        self.repository = repository or InMemoryEmailRepository()
        self.smtp_provider = smtp_provider or InMemorySmtpProvider()
        self.send_email_use_case = SendEmailUseCase(self.repository, self.smtp_provider)
        self.process_event_use_case = ProcessEventEmailUseCase(self.send_email_use_case)
        self.retry_use_case = RetryEmailUseCase(self.repository, self.smtp_provider)

    @classmethod
    def in_memory(cls) -> "EmailEventConsumer":
        return cls()

    def handle_event(self, event_type: str, payload: dict[str, object]):
        return self.process_event_use_case.execute(event_type=event_type, payload=payload)

    def retry_failed_message(self, message_id: str):
        return self.retry_use_case.execute(message_id)
