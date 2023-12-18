import django.contrib.auth.decorators
import django.contrib.auth.forms
import django.contrib.auth.models
import django.contrib.messages
import django.forms
import django.http
import django.shortcuts
import django.utils.decorators
import django.views.generic

import categories.models
import resume.models


class ResumeView(django.views.generic.ListView):
    model = resume.models.Resume
    template_name = "resume/resume.html"
    context_object_name = "resumes"
    paginate_by = 20

    def get_queryset(self):
        return self.model.objects.filter(is_active=True)


class ResumeCategoryView(ResumeView):
    def get_queryset(self):
        self.category = django.shortcuts.get_object_or_404(
            categories.models.Category,
            name=self.kwargs["category"],
        )
        return self.model.objects.filter(
            category=self.category,
            is_active=True,
        )


class ResumeSubcategoryView(ResumeView):
    def get_queryset(self):
        self.category = django.shortcuts.get_object_or_404(
            categories.models.Category,
            name=self.kwargs["category"],
        )
        self.subcategory = django.shortcuts.get_object_or_404(
            categories.models.Subcategory,
            name=self.kwargs["subcategory"],
        )

        return self.model.objects.filter(
            category=self.category,
            subcategory=self.subcategory,
            is_active=True,
        )


class ResumeDetailView(django.views.generic.DetailView):
    model = resume.models.Resume
    template_name = "resume/detail.html"
    context_object_name = "resume"


__all__ = []
