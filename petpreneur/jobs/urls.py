import django.urls

import jobs.views

app_name = "jobs"

urlpatterns = [
    django.urls.path(
        "create/",
        jobs.views.JobCreationView.as_view(),
        name="create",
    ),
]

__all__ = []
