import django.forms

import resume.models


class ResumeForm(django.forms.ModelForm):
    class Meta:
        model = resume.models.Resume
        fields = (model.text.field.name,)


__all__ = []
