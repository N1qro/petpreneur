import django.forms

import jobs.models


class DeleteJobForm(django.forms.ModelForm):
    class Meta:
        model = jobs.models.Job
        fields = [jobs.models.Job.id.field.name]
        widgets = {
            jobs.models.Job.id.field.name: django.forms.HiddenInput(),
        }


__all__ = []
