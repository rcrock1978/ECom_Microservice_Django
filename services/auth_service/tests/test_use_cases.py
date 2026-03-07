import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.auth_service.auth_service.settings')
import django
from django.test import TestCase
from django.core import mail

# must call setup before importing models or repos
django.setup()

from services.auth_service.infrastructure.repositories import UserRepository, RefreshTokenRepository
from services.auth_service.application.use_cases.register_user import register_user, RegistrationError
from services.auth_service.application.use_cases.login_user import login_user, AuthenticationError
from services.auth_service.application.use_cases.reset_password import reset_password, ResetError
from services.auth_service.auth_service.models import UserRole
from shared.message_bus import InMemoryMessageBus
from datetime import timedelta


class UseCaseTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # ensure tables exist by creating models directly (no migrations)

    def setUp(self):
        self.user_repo = UserRepository()
        self.token_repo = RefreshTokenRepository()
        self.bus = InMemoryMessageBus()

    def test_registration_and_duplicate(self):
        result = register_user("test@example.com", "password123",
                               user_repo=self.user_repo, bus=self.bus)
        self.assertEqual(result["email"], "test@example.com")
        # email was 'sent'
        self.assertEqual(len(mail.outbox), 1)
        # duplicate fails
        with self.assertRaises(RegistrationError):
            register_user("test@example.com", "password123", user_repo=self.user_repo)

    def test_login_and_lockout(self):
        register_user("login@a.com", "pass", user_repo=self.user_repo)
        with self.assertRaises(AuthenticationError):
            login_user("login@a.com", "wrong", user_repo=self.user_repo)
        user = self.user_repo.get_by_email("login@a.com")
        self.assertEqual(user.failed_attempts, 1)

        for _ in range(4):
            with self.assertRaises(AuthenticationError):
                login_user("login@a.com", "wrong", user_repo=self.user_repo)
        user.refresh_from_db()
        self.assertTrue(user.is_locked)
        with self.assertRaises(AuthenticationError):
            login_user("login@a.com", "pass", user_repo=self.user_repo)

    def test_password_reset_and_email(self):
        register_user("reset@a.com", "old", user_repo=self.user_repo)
        reset_password("reset@a.com", "new", user_repo=self.user_repo, bus=self.bus)
        self.assertEqual(len(mail.outbox), 2)
        tokens = login_user("reset@a.com", "new", user_repo=self.user_repo)
        self.assertIn("access_token", tokens)

    def test_admin_login(self):
        register_user("admin@a.com", "adminpass", role=UserRole.ADMIN, user_repo=self.user_repo)
        tokens = login_user("admin@a.com", "adminpass", is_admin=True, user_repo=self.user_repo)
        self.assertIn("access_token", tokens)
        register_user("user@a.com", "userpass", user_repo=self.user_repo)
        with self.assertRaises(AuthenticationError):
            login_user("user@a.com", "userpass", is_admin=True, user_repo=self.user_repo)

    def test_refresh_token_expiry(self):
        user = register_user("tk@a.com", "pwd", user_repo=self.user_repo)
        refresh = self.token_repo.create(user_id=user['id'], expires_delta=timedelta(seconds=-1))
        self.assertTrue(refresh.is_expired())
        self.token_repo.revoke(refresh)
        self.assertIsNone(self.token_repo.get(refresh.token))
