from emails.domain.entities import EmailMessage


class SendEmailUseCase:
    def __init__(self, repository: object, smtp_provider: object) -> None:
        self.repository = repository
        self.smtp_provider = smtp_provider

    def execute(self, to_email: str, subject: str, body_text: str, body_html: str, event_type: str) -> EmailMessage:
        message = EmailMessage.create(
            to_email=to_email,
            subject=subject,
            body_text=body_text,
            body_html=body_html,
            event_type=event_type,
        )
        self.repository.save(message)

        if self.smtp_provider.send(message):
            message.mark_sent()
        else:
            message.mark_failed()

        return self.repository.save(message)
