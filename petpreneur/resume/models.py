import django.db.models

import categories.models
import core.models
import resume.managers


class Resume(
    core.models.AbstractTextCreatedAtModel,
    core.models.AbstractIsActiveUserIdCategoryIdSubcategoryId,
):
    objects = resume.managers.ResumeManager()

    skills = django.db.models.ManyToManyField(
        categories.models.Skill,
        verbose_name="навыки",
        related_name="resume",
    )


__all__ = []
