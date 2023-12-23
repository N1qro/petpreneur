import django.conf
import django.contrib.messages
import django.core.mail
import django.http
import django.shortcuts
import django.views.generic

import feedback.forms as fb_forms


class FeedbackView(django.views.generic.TemplateView):
    template_name = "feedback/feedback.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if (
            "feedback_form" not in context
            and "feedback_extra_form" not in context
        ):
            feedback_extra_form = fb_forms.FeedbackExtraForm(
                self.request.POST or None,
            )

            feedback_form = fb_forms.FeedbackForm(self.request.POST or None)
            return context | {
                "feedback_form": feedback_form,
                "feedback_extra_form": feedback_extra_form,
            }

        return context

    def post(self, request: django.http.HttpRequest, *args, **kwargs):
        context = self.get_context_data()
        feedback_form = context["feedback_form"]
        feedback_extra_form = context["feedback_extra_form"]

        if feedback_form.is_valid() and feedback_extra_form.is_valid():
            mail = feedback_extra_form.cleaned_data.get("mail")
            text = feedback_form.cleaned_data.get("text")

            feedback_extra_form.save()
            fb = feedback_form.save(commit=False)
            fb.extra = feedback_extra_form.instance
            fb.save()

            django.core.mail.send_mail(
                "Обращение",
                text,
                django.conf.settings.MAILTO_EMAIL,
                [
                    mail,
                ],
                fail_silently=False,
            )

            django.contrib.messages.success(request, "Обращение отправлено!")

            return django.shortcuts.redirect("feedback:feedback")
        return django.shortcuts.render(request, self.template_name, context)


__all__ = []
