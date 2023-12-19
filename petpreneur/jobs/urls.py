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
        "",
        jobs.views.JobsView.as_view(),
        name="jobs",
    ),
    django.urls.path(
        "<int:pk>/",
        jobs.views.JobDetailView.as_view(),
        name="detail",
    ),
    django.urls.path(
        "<category>/",
        jobs.views.JobsCategoryView.as_view(),
        name="category",
    ),
    django.urls.path(
        "<category>/<subcategory>",
        jobs.views.JobsSubcategoryView.as_view(),
        name="subcategory",
    ),
]

__all__ = []
