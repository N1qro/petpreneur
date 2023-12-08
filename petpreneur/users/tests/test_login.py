import django.shortcuts
import django.test


class LogInTests(django.test.TestCase):
    def setUp(self):
        self.auth_data = {
            "username": "testuser",
            "email": "example@gmail.com",
            "password1": "12345678qwer",
            "password2": "12345678qwer",
        }

    def test_login_with_username(self):
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=self.auth_data,
        )
        self.client.logout()
        logged_in = self.client.login(
            username="testuser",
            password="12345678qwer",
        )
        self.assertTrue(logged_in)

        self.client.logout()
        logged_in = self.client.login(
            username="invalid username",
            password="invalid password",
        )

        self.assertFalse(logged_in)


__all__ = []
