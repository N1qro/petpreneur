import http

import django.contrib.auth
import django.contrib.auth.models
import django.core.mail
import django.shortcuts
import django.test
import django.utils.timezone
import freezegun


import users.models


class SignUpTests(django.test.TestCase):
    def setUp(self):
        self.auth_data = {
            "username": "testuser",
            "email": "example@gmail.com",
            "password1": "12345678qwer",
            "password2": "12345678qwer",
        }

    def test_signup_page_url(self):
        response = self.client.get(django.shortcuts.reverse("users:signup"))
        self.assertEqual(response.status_code, http.HTTPStatus.OK)

    def test_valid_signup_form(self):
        users_count = users.models.User.objects.count()

        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=self.auth_data,
        )

        self.assertEqual(
            users_count + 1,
            users.models.User.objects.count(),
        )

    def test_invalid_signup_form(self):
        users_count = users.models.User.objects.count()

        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data={},
        )

        self.assertEqual(
            users_count,
            users.models.User.objects.count(),
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_positive_activate_user(self):
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=self.auth_data,
        )

        self.assertEqual(
            users.models.User.objects.get(
                username="testuser",
            ).is_active,
            0,
        )

        signer = django.core.signing.TimestampSigner()
        response = self.client.get(
            django.shortcuts.reverse(
                "users:activate",
                args=[signer.sign("testuser")],
            ),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.FOUND)

        self.assertEqual(
            users.models.User.objects.get(
                username="testuser",
            ).is_active,
            1,
        )

    @django.test.override_settings(DEFAULT_USER_IS_ACTIVE=False)
    def test_negative_activate_user(self):
        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=self.auth_data,
        )

        signer = django.core.signing.TimestampSigner()
        username = signer.sign("testuser")

        with freezegun.freeze_time(
            django.utils.timezone.now()
            + django.utils.timezone.timedelta(days=1),
        ):
            response = self.client.get(
                django.shortcuts.reverse(
                    "users:activate",
                    args=[username],
                ),
            )

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

        self.assertEqual(
            users.models.User.objects.get(
                username="testuser",
            ).is_active,
            0,
        )

    def test_send_email_after_signup(self):
        mail_count = len(django.core.mail.outbox)

        self.client.post(
            django.shortcuts.reverse("users:signup"),
            data=self.auth_data,
        )

        self.assertEqual(len(django.core.mail.outbox), mail_count + 1)


__all__ = []
