class RetryEmailUseCase:
    def __init__(self, repository: object, smtp_provider: object, max_retries: int = 3) -> None:
        self.repository = repository
        self.smtp_provider = smtp_provider
        self.max_retries = max_retries

    def execute(self, message_id: str):
        message = self.repository.get_by_id(message_id)
        if not message:
            raise ValueError("Email message not found")

        while message.retry_count < self.max_retries:
            if self.smtp_provider.send(message):
                message.mark_sent()
                return self.repository.save(message)
            message.increment_retry()

        message.mark_failed()
        return self.repository.save(message)
