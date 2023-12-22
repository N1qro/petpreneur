import django.urls

import resume.views

app_name = "resume"

urlpatterns = [
    django.urls.path(
        "",
        resume.views.ResumeView.as_view(),
        name="resume_list",
    ),
    django.urls.path(
        "<int:pk>/",
        resume.views.ResumeDetailView.as_view(),
        name="detail",
    ),
]

__all__ = []
