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
        query = self.request.GET.get("q")
        if query:
            return self.model.objects.filter(
                django.db.models.Q(text__icontains=query),
            )

        return self.model.objects.filter(is_active=True)


class ResumeCategoryView(ResumeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        return context

    def get_queryset(self):
        self.category = django.shortcuts.get_object_or_404(
            categories.models.Category,
            name=self.kwargs["category"],
        )
        return (
            super()
            .get_queryset()
            .filter(
                category=self.category,
            )
        )


class ResumeSubcategoryView(ResumeView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.kwargs["category"]
        context["subcategory"] = self.kwargs["subcategory"]
        return context

    def get_queryset(self):
        self.category = django.shortcuts.get_object_or_404(
            categories.models.Category,
            name=self.kwargs["category"],
        )
        self.subcategory = django.shortcuts.get_object_or_404(
            categories.models.Subcategory,
            name=self.kwargs["subcategory"],
        )

        return (
            super()
            .get_queryset()
            .filter(
                category=self.category,
                subcategory=self.subcategory,
            )
        )


class ResumeDetailView(django.views.generic.DetailView):
    model = resume.models.Resume
    template_name = "resume/detail.html"
    context_object_name = "resume"


__all__ = []
