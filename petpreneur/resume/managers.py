import django.core
import django.db.models
import django.utils


import categories.models
import resume.models


class ResumeManager(django.db.models.Manager):
    def active(self):
        return self.get_queryset().filter(is_active=True)

    def skills(self):
        return (
            super()
            .get_queryset()
            .prefetch_related(
                django.db.models.Prefetch(
                    resume.models.Resume.skills.field.name,
                    queryset=categories.models.Skill.objects.only(
                        categories.models.Skill.name.field.name,
                    ),
                ),
            ),
        )


__all__ = []
