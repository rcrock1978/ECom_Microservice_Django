import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.auth_service.auth_service.settings')
import django
django.setup()

from django.test import Client, TestCase
from services.auth_service.infrastructure.repositories import UserRepository
from django.core import mail
from services.auth_service.domain.entities import UserRole


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # repository used by views is a global; clear for each test
        from services.auth_service.presentation import views
        views._user_repo = UserRepository()

    def test_register_endpoint(self):
        mail.outbox = []
        resp = self.client.post('/register/', {'email': 'v@a.com', 'password': 'pw'}, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['email'], 'v@a.com')
        self.assertEqual(len(mail.outbox), 1)

    def test_verify_email_endpoint(self):
        mail.outbox = []
        self.client.post('/register/', {'email': 'v4@a.com', 'password': 'pw'}, content_type='application/json')
        # extract token from email body
        body = mail.outbox[0].body
        token = body.split('/')[-1]
        resp = self.client.post('/verify/', {'token': token}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        # login now works
        resp2 = self.client.post('/login/', {'email': 'v4@a.com', 'password': 'pw'}, content_type='application/json')
        self.assertEqual(resp2.status_code, 200)

    def test_login_endpoint(self):
        # register first via endpoint
        self.client.post('/register/', {'email': 'v2@a.com', 'password': 'pwd'}, content_type='application/json')
        # verify using token from mail
        body = mail.outbox[0].body
        tok = body.split('/')[-1]
        self.client.post('/verify/', {'token': tok}, content_type='application/json')
        resp = self.client.post('/login/', {'email': 'v2@a.com', 'password': 'pwd'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access_token', resp.json())
        tokens = resp.json()
        # refresh afterwards
        resp3 = self.client.post('/refresh/', {'refresh_token': tokens['refresh_token']}, content_type='application/json')
        self.assertEqual(resp3.status_code, 200)
        new_tokens = resp3.json()
        self.assertIn('access_token', new_tokens)
        self.assertNotEqual(tokens['refresh_token'], new_tokens['refresh_token'])
        # logout
        resp4 = self.client.post('/logout/', {'refresh_token': new_tokens['refresh_token']}, content_type='application/json')
        self.assertEqual(resp4.status_code, 200)
        # further refresh should fail
        resp5 = self.client.post('/refresh/', {'refresh_token': new_tokens['refresh_token']}, content_type='application/json')
        self.assertEqual(resp5.status_code, 400)
    def test_password_reset_endpoint(self):
        mail.outbox = []
        self.client.post('/register/', {'email': 'v3@a.com', 'password': 'pwd'}, content_type='application/json')
        body = mail.outbox[0].body
        tok = body.split('/')[-1]
        self.client.post('/verify/', {'token': tok}, content_type='application/json')
        resp = self.client.post('/password-reset/', {'email': 'v3@a.com', 'new_password': 'new'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        # one email for registration and one for reset
        self.assertEqual(len(mail.outbox), 2)
        # login with new password
        resp2 = self.client.post('/login/', {'email': 'v3@a.com', 'password': 'new'}, content_type='application/json')
        self.assertEqual(resp2.status_code, 200)
