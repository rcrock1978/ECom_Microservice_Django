from django.test import Client, TestCase
from services.auth_service.infrastructure.repositories import UserRepository
from services.auth_service.domain.entities import UserRole


class AuthViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # repository used by views is a global; clear for each test
        from services.auth_service.presentation import views
        views._user_repo = UserRepository()

    def test_register_endpoint(self):
        resp = self.client.post('/register/', {'email': 'v@a.com', 'password': 'pw'}, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        data = resp.json()
        self.assertEqual(data['email'], 'v@a.com')

    def test_login_endpoint(self):
        # register first via endpoint
        self.client.post('/register/', {'email': 'v2@a.com', 'password': 'pwd'}, content_type='application/json')
        resp = self.client.post('/login/', {'email': 'v2@a.com', 'password': 'pwd'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        self.assertIn('access_token', resp.json())

    def test_password_reset_endpoint(self):
        self.client.post('/register/', {'email': 'v3@a.com', 'password': 'pwd'}, content_type='application/json')
        resp = self.client.post('/password-reset/', {'email': 'v3@a.com', 'new_password': 'new'}, content_type='application/json')
        self.assertEqual(resp.status_code, 200)
        # login with new password
        resp2 = self.client.post('/login/', {'email': 'v3@a.com', 'password': 'new'}, content_type='application/json')
        self.assertEqual(resp2.status_code, 200)
