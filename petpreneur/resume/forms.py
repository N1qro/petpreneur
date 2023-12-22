import django.contrib.messages
import django.forms

import categories.models
import resume.models


class ResumeForm(django.forms.ModelForm):
    class Meta:
        model = resume.models.Resume
        fields = (
            model.text.field.name,
            model.is_active.field.name,
        )

        labels = {
            model.is_active.field.name: "Опубликовано",
        }

        widgets = {
            model.text.field.name: django.forms.Textarea(attrs={"cols": None}),
        }


class ResumeSearchForm(django.forms.ModelForm):
    search_query = django.forms.CharField(required=False, label="Поиск")

    class Meta:
        model = resume.models.Resume
        fields = [
            model.category.field.name,
            model.subcategory.field.name,
        ]


class SkillAddForm(django.forms.ModelForm):
    def save(self):
        """
        Возвращает объект навыка и булево значение,
        обозначающее, был ли создан навык сейчас или нет
        """
        skill_name = self.data.get("name")
        if skill_name:
            skill, did_create = categories.models.Skill.get_or_create(
                skill_name,
            )
            if did_create:
                skill.save()
            self.instance = skill
            return skill, did_create
        raise Exception("SKILL NAME NOT PASSED")

    class Meta:
        model = categories.models.Skill
        fields = (model.name.field.name,)


__all__ = []
