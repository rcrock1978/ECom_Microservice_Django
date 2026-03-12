from pathlib import Path


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
