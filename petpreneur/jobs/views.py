import django.db.models
import django.urls
import django.views.generic

import categories.models
import jobs.forms
import jobs.models


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class JobCreationView(django.views.generic.FormView):
    template_name = "jobs/create.html"
    form_class = jobs.forms.CreateJobForm

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.user = self.request.user
        form_data.save()

        django.contrib.messages.success(
            self.request,
            "Новый проект успешно создан!",
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return django.urls.reverse("users:projects")


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class JobEditView(django.views.generic.UpdateView):
    template_name = "jobs/create.html"
    form_class = jobs.forms.CreateJobForm
    model = jobs.models.Job

    def form_valid(self, form):
        form_data = form.save(commit=False)
        form_data.user = self.request.user
        form_data.save()

        django.contrib.messages.success(
            self.request,
            "Проект успешно изменен!",
        )
        return super().form_valid(form)

    def get_success_url(self) -> str:
        return django.urls.reverse("users:projects")


class JobsView(django.views.generic.ListView):
    model = jobs.models.Job
    template_name = "jobs/jobs.html"
    context_object_name = "jobs"
    paginate_by = 12

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = jobs.forms.JobSearchForm(
            self.request.GET or None,
        )
        context["paginate_by"] = self.paginate_by
        return context

    def get_queryset(self):
        form = jobs.forms.JobSearchForm(self.request.GET or None)
        if form.is_valid():
            category = form.cleaned_data.get("category")
            subcategory = form.cleaned_data.get("subcategory")
            search_query = form.cleaned_data.get("search_query")
            print(category, subcategory, search_query)

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


class JobsCategoryView(JobsView):
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


class JobsSubcategoryView(JobsView):
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


class JobDetailView(django.views.generic.DetailView):
    model = jobs.models.Job
    template_name = "jobs/detail.html"
    context_object_name = "jobs"


__all__ = []
