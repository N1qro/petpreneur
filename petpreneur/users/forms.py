import django.contrib.auth.forms
import django.forms
import django.utils.safestring

import users.models


class UserCreationForm(
    django.contrib.auth.forms.UserCreationForm,
):
    class Meta(django.contrib.auth.forms.UserCreationForm.Meta):
        model = users.models.User
        fields = (model.username.field.name, model.email.field.name)


class PictureWidget(django.forms.widgets.FileInput):
    def render(self, name, value, attrs=None, **kwargs):
        input_html = super().render(name, value, attrs=None, **kwargs)
        if value:
            image_tmb = django.utils.safestring.mark_safe(
                f"<p class=text-center>{value.instance.image_tmb()}</p>",
            )
            return f"{image_tmb}{input_html}"
        return input_html


class UserChangeForm(
    django.contrib.auth.forms.UserChangeForm,
):
    password = None

    class Meta(django.contrib.auth.forms.UserChangeForm.Meta):
        model = users.models.User
        fields = (
            model.email.field.name,
            model.first_name.field.name,
            model.last_name.field.name,
            model.image.field.name,
            model.contacts.field.name,
        )

        labels = {
            model.image.field.name: "Аватарка",
        }

        widgets = {
            model.image.field.name: PictureWidget,
        }


__all__ = []
