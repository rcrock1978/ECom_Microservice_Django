from emails.infrastructure.repositories import InMemoryEmailRepository
from emails.presentation.serializers import serialize_email_message


class EmailAdminFacade:
    def __init__(self, repository: InMemoryEmailRepository) -> None:
        self.repository = repository

    def get_overview(self) -> dict[str, object]:
        messages = self.repository.list_messages()
        failed = self.repository.list_failed()
        return {
            "status": 200,
            "data": {
                "total_messages": len(messages),
                "failed_messages": len(failed),
            },
        }

    def list_failed_emails(self) -> dict[str, object]:
        failed = self.repository.list_failed()
        return {"status": 200, "data": [serialize_email_message(item) for item in failed]}

    def replay_failed(self) -> dict[str, object]:
        replayed = 0
        for message in self.repository.list_failed():
            message.status = "sent"
            self.repository.save(message)
            replayed += 1
        return {"status": 200, "data": {"replayed": replayed}}
