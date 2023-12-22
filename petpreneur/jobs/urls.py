import django.urls

import jobs.views

app_name = "jobs"

urlpatterns = [
    django.urls.path(
        "create/",
        jobs.views.JobCreationView.as_view(),
        name="create",
    ),
    django.urls.path(
        "edit/<int:pk>/",
        jobs.views.JobEditView.as_view(),
        name="edit",
    ),
    django.urls.path(
        "",
        jobs.views.JobsView.as_view(),
        name="jobs_list",
    ),
    django.urls.path(
        "<int:pk>/",
        jobs.views.JobDetailView.as_view(),
        name="detail",
    ),
]

__all__ = []
