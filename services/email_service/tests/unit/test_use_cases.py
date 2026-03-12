from emails.application.use_cases.process_event_email import ProcessEventEmailUseCase
from emails.application.use_cases.send_email import SendEmailUseCase
from emails.infrastructure.repositories import InMemoryEmailRepository
from emails.infrastructure.smtp_provider import InMemorySmtpProvider


def test_send_email_use_case_persists_message() -> None:
    repository = InMemoryEmailRepository()
    provider = InMemorySmtpProvider()
    use_case = SendEmailUseCase(repository, provider)

    message = use_case.execute(
        to_email="ray@example.com",
        subject="Welcome",
        body_text="Hi Ray",
        body_html="<p>Hi Ray</p>",
        event_type="user.registered",
    )

    assert message.status == "sent"
    assert len(repository.list_messages()) == 1


def test_process_event_email_uses_template_and_sends() -> None:
    repository = InMemoryEmailRepository()
    provider = InMemorySmtpProvider()
    send_email = SendEmailUseCase(repository, provider)
    process_event = ProcessEventEmailUseCase(send_email)

    message = process_event.execute(
        event_type="order.confirmed",
        payload={"email": "ray@example.com", "order_number": "ORD-1"},
    )

    assert message.subject == "Order Confirmation"
    assert "ORD-1" in message.body_text
