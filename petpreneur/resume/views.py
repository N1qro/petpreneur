import django.contrib.auth.decorators
import django.contrib.auth.forms
import django.contrib.auth.models
import django.contrib.messages
import django.forms
import django.http
import django.shortcuts
import django.utils.decorators
import django.views.generic

import resume.models
import resume.forms


class ResumeView(django.views.generic.ListView):
    model = resume.models.Resume
    template_name = "resume/resume.html"
    context_object_name = "resumes"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = resume.forms.ResumeSearchForm(
            self.request.GET or None,
        )
        context["paginate_by"] = self.paginate_by
        return context

    def get_queryset(self):
        form = resume.forms.ResumeSearchForm(self.request.GET or None)
        if form.is_valid():
            category = form.cleaned_data.get("category")
            subcategory = form.cleaned_data.get("subcategory")
            search_query = form.cleaned_data.get("search_query")
            queryset = self.model.objects.filter(is_active=True)

            if category:
                queryset = queryset.filter(category=category)
                if subcategory:
                    queryset = queryset.filter(subcategory=subcategory)

            if search_query:
                queryset = queryset.filter(
                    django.db.models.Q(title__icontains=search_query)
                    | django.db.models.Q(text__icontains=search_query),
                )

            return queryset  # noqa R504

        return self.model.objects.filter(is_active=True)


class ResumeDetailView(django.views.generic.DetailView):
    model = resume.models.Resume
    template_name = "resume/detail.html"
    context_object_name = "resume"


__all__ = []
