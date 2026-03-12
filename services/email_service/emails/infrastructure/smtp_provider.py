class InMemorySmtpProvider:
    def __init__(self, fail_attempts: int = 0) -> None:
        self.fail_attempts = fail_attempts
        self.attempts = 0

    def send(self, _: object) -> bool:
        self.attempts += 1
        if self.attempts <= self.fail_attempts:
            return False
        return True
