from auth.application.crypto import PasswordHasher
from auth.domain.entities import User
from auth.domain.value_objects import PasswordPolicy


class RegisterUserUseCase:
    def __init__(self, repository: object, event_publisher: object | None = None) -> None:
        self.repository = repository
        self.hasher = PasswordHasher()
        self.event_publisher = event_publisher

    def execute(self, name: str, email: str, password: str) -> User:
        if not PasswordPolicy.is_valid(password):
            raise ValueError("Weak password")
        if self.repository.get_user_by_email(email):
            raise ValueError("Email already exists")
        user = User.create(name=name, email=email, password_hash=self.hasher.hash(password))
        self.repository.save_user(user)
        if self.event_publisher:
            self.event_publisher.user_registered(user.id, user.email, user.name)
        return user
