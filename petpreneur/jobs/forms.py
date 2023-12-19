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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[jobs.models.Job.category.field.name].required = True
        self.fields[jobs.models.Job.subcategory.field.name].required = True

    class Meta:
        model = jobs.models.Job
        fields = [
            model.title.field.name,
            model.category.field.name,
            model.subcategory.field.name,
            model.text.field.name,
            model.image.field.name,
            model.is_active.field.name,
        ]
        labels = {
            model.is_active.field.name: "Опубликовать сразу",
        }


__all__ = []
