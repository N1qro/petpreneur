import django.urls

import home.views


urlpatterns = [
    django.urls.path("", home.views.home),
]
