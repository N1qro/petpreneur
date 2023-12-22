import django.contrib.messages
import django.db.models
import django.http
import django.shortcuts
import django.urls
import django.views.generic


import jobs.forms
import jobs.models
import resume.forms
import users.models


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
class JobEditView(django.views.generic.TemplateView):
    template_name = "jobs/edit.html"
    context_object_name = "skills"

    def get_job_model(self, pk):
        return jobs.models.Job.objects.get(pk=pk)

    def get(self, request, *args, **kwargs):
        if (
            jobs.models.Job.objects.get(pk=kwargs["pk"]).user
            != self.request.user
        ):
            django.contrib.messages.error(
                request,
                "Вы не можете изменять чужие проекты",
            )
            return django.shortcuts.redirect("users:projects")
        return super().get(request, *args, **kwargs)

    def post(self, request, pk):
        if "info_change" in request.POST:
            form = jobs.forms.CreateJobForm(
                request.POST or None,
                instance=self.get_job_model(pk),
            )
            if form.is_valid():
                form.save()
                django.contrib.messages.success(
                    request,
                    "Данные о проекте успешно изменены!",
                )
            else:
                django.contrib.messages.error(
                    request,
                    "Что-то пошло не так...",
                )
            return django.shortcuts.redirect("users:projects")
        elif "skill_add" in request.POST:
            form = resume.forms.SkillAddForm(request.POST or None)
            skill, was_created = form.save()

            job_model = self.get_job_model(pk)
            if job_model.skills.filter(id=skill.id).exists():
                django.contrib.messages.error(
                    request,
                    "Этот навык уже был добавлен в проект!",
                )
            else:
                job_model.skills.add(skill)
                django.contrib.messages.success(
                    request,
                    f'Навык "{skill.name}" успешно добавлен',
                )
        elif "skill_delete" in request.POST:
            skill_name = request.POST.get("skill_delete")
            job_model = self.get_job_model(pk)
            skill = job_model.skills.filter(name=skill_name).first()
            if not skill:
                django.contrib.messages.error(
                    request,
                    "Что-то пошло не так...",
                )
            else:
                job_model.skills.remove(skill)
                django.contrib.messages.info(
                    request,
                    f'Навык "{skill.name}" был успешно удалён',
                )

        return self.get(request, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_job = jobs.models.Job.objects.get(pk=context.get("pk"))
        context["form"] = jobs.forms.CreateJobForm(instance=current_job)
        context["skills"] = current_job.skills
        context["skill_form"] = resume.forms.SkillAddForm()
        return context


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


class JobDetailView(django.views.generic.DetailView):
    model = jobs.models.Job
    template_name = "jobs/detail.html"
    context_object_name = "job"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        job_object = context[self.context_object_name]
        resume_object = self.request.user.resume_set.first()

        context["form"] = jobs.forms.JobApplyForm()
        context["application"] = (
            jobs.models.JobRequests.objects.filter(
                job=job_object,
                resume=resume_object,
            )
            .select_related("job")
            .select_related("job__user")
            .first()
        )

        return context

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related(self.model.user.field.name)
            .only(
                self.model.text.field.name,
                self.model.image.field.name,
                self.model.title.field.name,
                f"{self.model.user.field.name}"
                f"__{users.models.User.contacts.field.name}",
            )
        )

    def post(self, request, pk):
        form = jobs.forms.JobApplyForm(request.POST or None)
        if form.is_valid():
            job_object = self.model.objects.get(pk=pk)
            if job_object.user == request.user:
                raise django.http.Http404(
                    "Вы не можете оставить заявку на свой же проект!",
                )

            try:
                new_request = jobs.models.JobRequests.objects.create(
                    resume=request.user.resume_set.first(),
                    job=job_object,
                    text=form.cleaned_data["text"],
                )
                new_request.save()
            except django.db.IntegrityError:
                raise django.http.Http404(
                    "Вы уже подавали заявку на этот проект!",
                )
            else:
                django.contrib.messages.success(
                    request,
                    "Заявка на проект успешно подана!",
                )
                return django.shortcuts.redirect("jobs:detail", pk=pk)
        raise Exception("VALIDATION ERROR")


__all__ = []
