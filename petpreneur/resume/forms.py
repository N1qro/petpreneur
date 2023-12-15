import django.forms

import resume.models


class ResumeForm(django.forms.ModelForm):
    class Meta:
        model = resume.models.Resume
        fields = ("text",)


__all__ = []
