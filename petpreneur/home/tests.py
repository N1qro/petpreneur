import http

import django.test
import django.urls


class StaticURLTests(django.test.TestCase):
    def test_homepage_endpoint(self):
        response = django.test.Client().get(
            django.urls.reverse("home:home"),
        )
        self.assertEqual(response.status_code, http.HTTPStatus.OK)


__all__ = []
