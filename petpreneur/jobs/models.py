import django.db.models
import django.utils.timezone

import categories.models
import core.models
import resume.models


class Job(
    core.models.AbstractTextCreatedAtModel,
    core.models.AbstractIsActiveUserIdCategoryIdSubcategoryId,
):
    default_image_url = (
        "https://abrakadabra.fun/uploads/posts/2021-12/"
        "1639258991_5-abrakadabra-fun-p-znak-voprosa-na-chernom-fone-5.png"
    )

    def _job_image_upload_to(self, filename):
        return (
            f"jobs/images/"
            f"{self.user_id}_{django.utils.timezone.now().day}/{filename}"
        )

    title = django.db.models.CharField(
        max_length=200,
        verbose_name="название",
    )

    image = django.db.models.ImageField(
        upload_to=_job_image_upload_to,
        verbose_name="изображение",
        blank=True,
    )

    skills = django.db.models.ManyToManyField(
        categories.models.Skill,
        verbose_name="навыки",
        related_name="job",
    )

    class Meta:
        verbose_name = "работа"
        verbose_name_plural = "работы"

    def __str__(self) -> str:
        if len(str(self.text)) > 20:
            return f"{self.text[:20]}..."
        return self.text[:20]


class JobRequests(core.models.AbstractTextCreatedAtModel):
    status = django.db.models.IntegerField(
        choices=(
            (1, "Отправлено"),
            (2, "Одобрено"),
            (3, "Отклонено"),
        ),
        verbose_name="статус",
        default=1,
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

    class Meta:
        verbose_name = "заявка"
        verbose_name_plural = "заявки"

    def __str__(self) -> str:
        if len(str(self.text)) > 20:
            return f"{self.text[:20]}..."
        return self.text[:20]


__all__ = []
