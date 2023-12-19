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
        blank=True,
    )

    class Meta:
        verbose_name = "резюме"
        verbose_name_plural = "резюме"

    def __str__(self) -> str:
        return self.user.username


__all__ = []
