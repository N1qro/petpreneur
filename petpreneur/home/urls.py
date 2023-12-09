import django.urls

import home.views

app_name = "home"

urlpatterns = [
    django.urls.path("", home.views.home, name="home"),
]
