from emails.domain.entities import EmailMessage


class InMemoryEmailRepository:
    def __init__(self) -> None:
        self._messages: dict[str, EmailMessage] = {}

    def save(self, message: EmailMessage) -> EmailMessage:
        self._messages[message.id] = message
        return message

    def get_by_id(self, message_id: str) -> EmailMessage | None:
        return self._messages.get(message_id)

    def list_messages(self) -> list[EmailMessage]:
        return list(self._messages.values())

    def list_failed(self) -> list[EmailMessage]:
        return [m for m in self._messages.values() if m.status == "failed"]
