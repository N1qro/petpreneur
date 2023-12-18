import django.conf
import django.conf.urls.static
import django.contrib.admin
import django.contrib.auth.urls
import django.urls

urlpatterns = [
    django.urls.path("", django.urls.include("home.urls")),
    django.urls.path("auth/", django.urls.include("users.urls")),
    django.urls.path("auth/", django.urls.include(django.contrib.auth.urls)),
    django.urls.path("jobs/", django.urls.include("jobs.urls")),
    django.urls.path("resume/", django.urls.include("resume.urls")),
    django.urls.path("admin/", django.contrib.admin.site.urls),
    django.urls.path("feedback/", django.urls.include("feedback.urls")),
]

if django.conf.settings.DEBUG:
    import debug_toolbar

    urlpatterns += (
        django.urls.path(
            "__debug__/",
            django.urls.include(debug_toolbar.urls),
        ),
    )
    urlpatterns += django.conf.urls.static.static(
        django.conf.settings.MEDIA_URL,
        document_root=django.conf.settings.MEDIA_ROOT,
    )
