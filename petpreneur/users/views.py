import django.conf
import django.contrib.auth.decorators
import django.contrib.auth.forms
import django.contrib.auth.models
import django.contrib.messages
import django.contrib.sites.shortcuts
import django.core.mail
import django.core.signing
import django.forms
import django.http
import django.shortcuts
import django.urls
import django.utils.decorators
import django.utils.timezone
import django.views.generic

import jobs.forms
import jobs.models
import resume.forms
import resume.models
import users.forms
import users.models


class SignUpView(
    django.views.generic.FormView,
):
    template_name = "users/signup.html"
    form_class = users.forms.UserCreationForm

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")

        form_save = form.save(commit=False)
        form_save.is_active = django.conf.settings.DEFAULT_USER_IS_ACTIVE
        form_save.save()

        user_resume = resume.models.Resume(
            is_active=False,
            text="Начинающий специалист...",
            user=form_save,
        )
        user_resume.save()

        signer = django.core.signing.TimestampSigner()

        url_to_activate = django.urls.reverse(
            "users:activate",
            args=[signer.sign(username)],
        )

        django.core.mail.send_mail(
            "Активация аккаунта",
            f"Для активации вашего аккаунта перейдите по ссылке:"
            f"\n{self.request.build_absolute_uri(url_to_activate)}",
            django.conf.settings.MAIL,
            [
                email,
            ],
            fail_silently=False,
        )
        django.contrib.messages.success(
            self.request,
            "Активируйте аккаунт перейдя по ссылке в почте!",
        )
        return super().form_valid(form)

    def get_success_url(self):
        return django.urls.reverse("users:signup")


class ActivateView(django.views.generic.RedirectView):
    pattern_name = "users:login"

    def get_redirect_url(self, *args, **kwargs):
        try:
            signer = django.core.signing.TimestampSigner()
            username = signer.unsign(
                self.kwargs["username"],
                max_age=django.utils.timezone.timedelta(hours=12),
            )

            user = django.shortcuts.get_object_or_404(
                users.models.User,
                username=username,
            )

            user.is_active = True
            user.save()

            django.contrib.messages.success(
                self.request,
                "Вы успешно активировали аккаунт",
            )
            return super().get_redirect_url()

        except django.core.signing.SignatureExpired:
            raise django.http.Http404()


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileResumeView(django.views.generic.TemplateView):
    template_name = "users/profile/resumes.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "form" not in context:
            resume_object = resume.models.Resume.objects.get(
                user=self.request.user,
            )

            form = resume.forms.ResumeForm(
                self.request.POST or None,
                instance=resume_object,
            )
            context["form"] = form

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        form = context["form"]

        if "form" in request.POST and form.is_valid():
            form.save()
        else:
            return django.shortcuts.render(
                request,
                self.template_name,
                context,
            )

        return django.shortcuts.redirect(django.urls.reverse("users:resumes"))


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileRequestsView(django.views.generic.ListView):
    model = jobs.models.JobRequests
    template_name = "users/profile/requests.html"
    context_object_name = "jobs"

    def post(self, request):
        job_request_id = request.POST.get("id")
        if job_request_id:
            try:
                job_request = django.shortcuts.get_object_or_404(
                    self.model,
                    id=job_request_id,
                )
                job_request.delete()
            except django.http.Http404:
                django.contrib.messages.error(
                    request,
                    "Во время отмены возникла ошибка. Попробуйте позднее",
                )
            else:
                django.contrib.messages.success(
                    request,
                    "Заявка была успешно отозвана",
                )

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button_text"] = "Отозвать"
        context["tab_label"] = "Отправленные заявки"
        return context

    def get_queryset(self):
        return users.models.User.objects.get_request_jobs(self.request.user.pk)


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileParticipateView(django.views.generic.ListView):
    model = jobs.models.JobRequests
    template_name = "users/profile/participating.html"
    context_object_name = "jobs"

    def post(self, request):
        job_id = request.POST.get("id")
        if job_id:
            try:
                return django.shortcuts.redirect(
                    django.urls.reverse("jobs:job", args=[job_id]),
                )

            except django.http.Http404:
                django.contrib.messages.error(
                    request,
                    "Возникла ошибка. Попробуйте позднее",
                )

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button_text"] = "Детали"
        context["tab_label"] = "Проекты, в которых я состою"
        return context

    def get_queryset(self):
        return users.models.User.objects.get_current_jobs(self.request.user.pk)


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileView(django.views.generic.TemplateView):
    template_name = "users/profile/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            "password_change" not in context
            and "user_contacts" not in context
            and "user_change" not in context
        ):
            password_change_form = (
                django.contrib.auth.forms.PasswordChangeForm(
                    user=self.request.user,
                    data=self.request.POST or None,
                )
            )
            user_contacts_form = users.forms.UserContactsForm(
                instance=self.request.user,
                data=self.request.POST or None,
            )
            user_change_form = users.forms.UserChangeForm(
                instance=self.request.user,
                data=self.request.POST or None,
                files=self.request.FILES or None,
            )

            context["password_change"] = password_change_form
            context["contacts_change"] = user_contacts_form
            context["user_change"] = user_change_form

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()

        password_change_form = context["password_change"]
        user_contacts_form = context["contacts_change"]
        user_change_form = context["user_change"]

        if (
            "password_change" in request.POST
            and password_change_form.is_valid()
        ):
            password_change_form.save()
            django.contrib.messages.add_message(
                request,
                django.contrib.messages.SUCCESS,
                "Проверьте почту, там лежит ссылка",
            )
        elif (
            "contacts_change" in request.POST and user_contacts_form.is_valid()
        ):
            user_contacts_form.save()
            django.contrib.messages.add_message(
                request,
                django.contrib.messages.SUCCESS,
                "Контакты успешно изменены!",
            )
        elif "user_change" in request.POST:
            if user_change_form.is_valid():
                user_change_form.save()
                django.contrib.messages.add_message(
                    request,
                    django.contrib.messages.SUCCESS,
                    "Данные пользователя успешно изменены!",
                )
        else:
            return django.shortcuts.render(
                request,
                self.template_name,
                context,
            )
        return django.shortcuts.redirect(django.urls.reverse("users:profile"))


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileProjectsView(django.views.generic.ListView):
    model = jobs.models.Job
    template_name = "users/profile/project_view.html"
    context_object_name = "jobs"

    def post(self, request):
        job_id = request.POST.get("id")
        if job_id:
            try:
                job = django.shortcuts.get_object_or_404(
                    self.model,
                    id=job_id,
                    user_id=request.user.id,
                )
                job.delete()
            except django.http.Http404:
                django.contrib.messages.error(
                    request,
                    "Во время удаления возникла ошибка. Попробуйте позднее",
                )
            else:
                django.contrib.messages.success(
                    request,
                    "Проект был успешно закрыт",
                )

        return self.get(request)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["button_text"] = "Удалить"
        context["tab_label"] = "Созданные мной проекты"
        return context

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).only(
            self.model.title.field.name,
            self.model.text.field.name,
            self.model.created_at.field.name,
        )


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileRecruitView(django.views.generic.ListView):
    template_name = "users/profile/recruit.html"


__all__ = []
