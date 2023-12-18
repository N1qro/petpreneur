import django.urls

import resume.views

app_name = "resume"

urlpatterns = [
    django.urls.path(
        "",
        resume.views.ResumeView.as_view(),
        name="resume",
    ),
    django.urls.path(
        "<int:pk>/",
        resume.views.ResumeDetailView.as_view(),
        name="detail",
    ),
    django.urls.path(
        "<category>/",
        resume.views.ResumeCategoryView.as_view(),
        name="category",
    ),
    django.urls.path(
        "<category>/<subcategory>",
        resume.views.ResumeSubcategoryView.as_view(),
        name="subcategory",
    ),
]

__all__ = []
