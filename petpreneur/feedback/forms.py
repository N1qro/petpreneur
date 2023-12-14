import django.forms

import feedback.models


class FeedbackForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.Feedback

        exclude = ["created_at", "status", "extra"]

        labels = {
            model.text.field.name: "Текст обращения",
        }

        help_texts = {
            model.text.field.name: "Введите текст обращение",
        }

        widgets = {
            model.text.field.name: django.forms.Textarea(
                attrs={"type": "text", "rows": 3},
            ),
        }


class FeedbackExtraForm(django.forms.ModelForm):
    class Meta:
        model = feedback.models.FeedbackExtra

        exclude = []

        labels = {
            model.mail.field.name: "Почта",
            model.name.field.name: "Имя",
        }

        help_texts = {
            model.name.field.name: "Введите ваше имя",
            model.mail.field.name: "Введите вашу почту",
        }

        widgets = {
            model.mail.field.name: django.forms.EmailInput(
                attrs={
                    "placeholder": "name@example.com",
                },
            ),
        }


__all__ = []
