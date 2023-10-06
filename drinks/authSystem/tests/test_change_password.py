from django.contrib.auth.models import User
from django.test import Client
from django.test.testcases import TestCase
from django.urls import reverse


class TestChangePassword(TestCase):

    def setUp(self):
        self.password = 'test123456'
        self.new_password = 'newabc123456'
        self.too_simple_password = 'abc'
        self.incorrect_password = '123456test'
        self.valid_form = {
            'old_password': self.password,
            'new_password1': self.new_password,
            'new_password2': self.new_password,
        }

        self.user = User.objects.create_user(username='testuser', password=self.password)
        self.client.login(username='testuser', password=self.password)

    def test_get_change_password_form(self):
        response = self.client.get(reverse('change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_change_password_when_positive_credentials(self):
        response = self.client.post(reverse('change_password'), data=self.valid_form)
        self.assertRedirects(response, '/', status_code=302, target_status_code=200)

    def test_change_password_new_password_too_simple(self):
        password_too_simple_form = dict(self.valid_form)
        password_too_simple_form['new_password1'] = self.too_simple_password
        password_too_simple_form['new_password2'] = self.too_simple_password

        response = self.client.post(reverse('change_password'), data=password_too_simple_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_change_password_old_password_incorrect(self):
        old_password_incorrect_form = dict(self.valid_form)
        old_password_incorrect_form['old_password'] = self.incorrect_password

        response = self.client.post(reverse('change_password'), data=old_password_incorrect_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_change_password_new_passwords_not_match(self):
        passwords_not_match_form = dict(self.valid_form)
        passwords_not_match_form['new_password1'] = self.password
        passwords_not_match_form['new_password2'] = self.new_password

        response = self.client.post(reverse('change_password'), data=passwords_not_match_form)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')

    def test_method_not_allowed(self):
        methods = [
            Client.delete,
            Client.put,
            Client.patch,
        ]

        for method in methods:
            with self.subTest(method=method):
                response = method(self.client, (reverse('change_password')))
                self.assertEqual(response.status_code, 405)
