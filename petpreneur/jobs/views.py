import django.urls
import django.views.generic

import jobs.forms


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


__all__ = []
