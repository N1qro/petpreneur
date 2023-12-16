import django.urls

import home.views

app_name = "home"

urlpatterns = [
    django.urls.path("", home.views.HomeView.as_view(), name="home"),
]
