from django.contrib.auth.models import User
from django.test import Client
from django.test.testcases import TestCase
from django.urls import reverse


class TestLogin(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='123')

    def test_get_login_form(self):
        response = self.client.get(reverse('login_user'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_user.html')

    def test_login_when_positive_credentials(self):
        response = self.client.post(reverse('login_user'), data={'username': 'testuser', 'password': '123'})
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_login_when_incorrect_password(self):
        response = self.client.post(reverse('login_user'), data={'username': 'testuser', 'password': 'abc'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_user.html')

    def test_login_when_incorrect_username(self):
        response = self.client.post(reverse('login_user'), data={'username': 'testuser2', 'password': '123'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login_user.html')

    def test_method_not_allowed(self):
        methods = [
            Client.delete,
            Client.put,
            Client.patch,
        ]

        for method in methods:
            with self.subTest(method=method):
                response = method(self.client, (reverse('login_user')))
                self.assertEqual(response.status_code, 405)
