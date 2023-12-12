import django.conf
import django.contrib.auth.decorators
import django.contrib.auth.models
import django.contrib.messages
import django.contrib.sites.shortcuts
import django.core.mail
import django.core.signing
import django.http
import django.shortcuts
import django.utils.decorators
import django.utils.timezone
import django.views.generic

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


@django.utils.decorators.method_decorator(
    django.contrib.auth.decorators.login_required,
    name="dispatch",
)
class ProfileView(django.views.generic.TemplateView):
    template_name = "users/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if "forms" not in context:
            forms = (
                users.forms.UserChangeForm(
                    self.request.POST or None,
                    self.request.FILES or None,
                    instance=self.request.user,
                ),
            )
            context["forms"] = forms
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        if all(form.is_valid() for form in context["forms"]):
            [form.save() for form in context["forms"]]
            return django.shortcuts.redirect(
                django.shortcuts.reverse("users:profile"),
            )
        return django.shortcuts.render(request, self.template_name, context)


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


@django.contrib.auth.decorators.login_required()
def resume_view(request: django.http.HttpRequest):
    context = {}
    template_name = "users/profile/resumes.html"
    return django.shortcuts.render(request, template_name, context)


@django.contrib.auth.decorators.login_required()
def requests_view(request: django.http.HttpRequest):
    context = {}
    template_name = "users/profile/requests.html"
    return django.shortcuts.render(request, template_name, context)


@django.contrib.auth.decorators.login_required()
def participate_view(request: django.http.HttpRequest):
    context = {}
    template_name = "users/profile/participating.html"
    return django.shortcuts.render(request, template_name, context)


@django.contrib.auth.decorators.login_required()
def profile_view(request: django.http.HttpRequest):
    context = {}
    template_name = "users/profile/profile.html"
    return django.shortcuts.render(request, template_name, context)


@django.contrib.auth.decorators.login_required()
def projects_view(request: django.http.HttpRequest):
    context = {}
    template_name = "users/profile/projects.html"
    return django.shortcuts.render(request, template_name, context)


@django.contrib.auth.decorators.login_required()
def recruit_view(request: django.http.HttpRequest):
    context = {}
    template_name = "users/profile/recruit.html"
    return django.shortcuts.render(request, template_name, context)


__all__ = []
