from emails.application.use_cases.retry_email import RetryEmailUseCase
from emails.domain.entities import EmailMessage
from emails.infrastructure.repositories import InMemoryEmailRepository
from emails.infrastructure.smtp_provider import InMemorySmtpProvider


def test_retry_policy_succeeds_on_second_attempt() -> None:
    repository = InMemoryEmailRepository()
    provider = InMemorySmtpProvider(fail_attempts=1)
    use_case = RetryEmailUseCase(repository, provider)

    message = EmailMessage.create(
        to_email="ray@example.com",
        subject="Retry",
        body_text="Body",
        body_html="<p>Body</p>",
        event_type="email.retry",
    )
    repository.save(message)

    retried = use_case.execute(message.id)

    assert retried.status == "sent"
    assert retried.retry_count == 1


def test_retry_policy_marks_failed_after_limit() -> None:
    repository = InMemoryEmailRepository()
    provider = InMemorySmtpProvider(fail_attempts=5)
    use_case = RetryEmailUseCase(repository, provider, max_retries=2)

    message = EmailMessage.create(
        to_email="ray@example.com",
        subject="Retry",
        body_text="Body",
        body_html="<p>Body</p>",
        event_type="email.retry",
    )
    repository.save(message)

    retried = use_case.execute(message.id)

    assert retried.status == "failed"
    assert retried.retry_count == 2
