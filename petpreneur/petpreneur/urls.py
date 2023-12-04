import django.contrib.admin
import django.urls


urlpatterns = [
    django.urls.path("", django.urls.include("home.urls")),
    django.urls.path("admin/", django.contrib.admin.site.urls),
]
