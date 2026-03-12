from pathlib import Path


class ProcessEventEmailUseCase:
    def __init__(self, send_email_use_case: object) -> None:
        self.send_email_use_case = send_email_use_case

    def _template_body(self, template_name: str, **values: object) -> str:
        template_dir = Path(__file__).resolve().parents[2] / "infrastructure" / "templates"
        template = (template_dir / template_name).read_text(encoding="utf-8")
        return template.format(**values)

    def execute(self, event_type: str, payload: dict[str, object]):
        if event_type == "order.confirmed":
            subject = "Order Confirmation"
            body_text = self._template_body("order_confirmation.txt", order_number=payload.get("order_number", ""))
            body_html = self._template_body("order_confirmation.html", order_number=payload.get("order_number", ""))
        elif event_type == "reward.points_credited":
            subject = "Reward Points Added"
            body_text = self._template_body("reward_points_credited.txt", points=payload.get("points", 0))
            body_html = self._template_body("reward_points_credited.html", points=payload.get("points", 0))
        else:
            subject = "Notification"
            body_text = "You have a new notification."
            body_html = "<p>You have a new notification.</p>"

        return self.send_email_use_case.execute(
            to_email=str(payload.get("email", "")),
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            event_type=event_type,
        )
