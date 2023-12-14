import django.db.models
import django.utils.timezone

import core.models


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


__all__ = []
