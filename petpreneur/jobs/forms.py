import django.forms

import jobs.models


class DeleteJobForm(django.forms.ModelForm):
    class Meta:
        model = jobs.models.Job
        fields = [jobs.models.Job.id.field.name]
        widgets = {
            jobs.models.Job.id.field.name: django.forms.HiddenInput(),
        }


class CreateJobForm(django.forms.ModelForm):
    class Meta:
        model = jobs.models.Job
        fields = [
            jobs.models.Job.title.field.name,
            jobs.models.Job.text.field.name,
            jobs.models.Job.image.field.name,
            jobs.models.Job.is_active.field.name,
        ]
        labels = {
            jobs.models.Job.is_active.field.name: "Опубликовать сразу",
        }


__all__ = []
