from auth.application.crypto import PasswordHasher
from auth.domain.value_objects import PasswordPolicy


class ResetPasswordUseCase:
    def __init__(self, repository: object) -> None:
        self.repository = repository
        self.hasher = PasswordHasher()

    def execute(self, token: str, new_password: str) -> None:
        if not PasswordPolicy.is_valid(new_password):
            raise ValueError("Weak password")

        matching_email = None
        for email, stored in self.repository.reset_tokens.items():
            if stored == token:
                matching_email = email
                break

        if not matching_email:
            raise ValueError("Invalid reset token")

        user = self.repository.get_user_by_email(matching_email)
        if not user:
            raise ValueError("User not found")

        user.password_hash = self.hasher.hash(new_password)
        self.repository.save_user(user)
