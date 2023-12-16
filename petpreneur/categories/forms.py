import django.contrib.auth.forms
import django.forms
import django.utils.safestring

import categories.models


class SkillChangeForm(django.forms.ModelForm):
    class Meta:
        model = categories.models.Skill
        fields = (model.name.field.name,)

        labels = {
            model.name.field.name: "Навыки",
        }


__all__ = []
