import django.db.models
import django.utils.timezone

import categories.models
import core.models
import resume.models


class Job(
    core.models.AbstractTextCreatedAtModel,
    core.models.AbstractIsActiveUserIdCategoryIdSubcategoryId,
):
    def _job_image_upload_to(self, filename):
        return (
            f"jobs/images/"
            f"{self.user_id}_{django.utils.timezone.now().day}/{filename}"
        )

    image = django.db.models.ImageField(
        upload_to=_job_image_upload_to,
        verbose_name="изображение",
    )

    skills = django.db.models.ManyToManyField(
        categories.models.Skill,
        verbose_name="навыки",
        related_name="job",
    )


class JobRequests(core.models.AbstractTextCreatedAtModel):
    status = django.db.models.IntegerField(
        choices=(
            (1, "Отправлено"),
            (2, "Одобрено"),
            (3, "Отклонено"),
        ),
        verbose_name="статус",
    )

    resume = django.db.models.ForeignKey(
        resume.models.Resume,
        on_delete=django.db.models.CASCADE,
        related_name="job_requests",
        verbose_name="резюме",
    )

    job = django.db.models.ForeignKey(
        Job,
        on_delete=django.db.models.CASCADE,
        related_name="job_requests",
        verbose_name="работа",
    )


__all__ = []
