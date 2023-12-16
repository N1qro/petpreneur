import django.contrib.auth.models
import django.db.models
import sorl.thumbnail

import users.manager


class User(django.contrib.auth.models.AbstractUser):
    def _profile_imgae_upload_to(self, filename):
        return f"users/images/{self.id}/{filename}"

    email = django.db.models.EmailField(
        verbose_name="почта",
        unique=True,
    )

    image = django.db.models.ImageField(
        upload_to=_profile_imgae_upload_to,
        verbose_name="аватарка",
        null=True,
        blank=True,
    )

    contacts = django.db.models.TextField(
        verbose_name="контакты",
        blank=True,
        null=True,
    )

    REQUIRED_FIELDS = ["email"]

    objects = users.manager.UserManager()

    def image_tmb(self):
        if self.image:
            return django.utils.html.mark_safe(
                f'<img src="{self.get_image_300x300().url}" width="150">',
            )
        return "Нет изображения"

    def get_image_300x300(self):
        return sorl.thumbnail.get_thumbnail(
            self.image,
            "300x300",
            crop="center",
            quality=51,
        )

    image_tmb.short_description = "превью"
    image_tmb.allow_tags = True

    def __str__(self):
        return self.username


__all__ = []
