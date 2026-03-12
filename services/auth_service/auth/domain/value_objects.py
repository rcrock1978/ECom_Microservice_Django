import re


class EmailAddress:
    def __init__(self, value: str) -> None:
        normalized = value.strip().lower()
        if "@" not in normalized:
            raise ValueError("Invalid email")
        self.value = normalized


class PasswordPolicy:
    @staticmethod
    def is_valid(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"\d", password):
            return False
        return True
