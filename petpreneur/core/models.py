import django.db.models


class AbstractNameSlugModel(django.db.models.Model):
    name = django.db.models.CharField(
        verbose_name="имя",
        max_length=150,
        help_text="Максимальная длина - 150 символов",
        unique=True,
    )

    slug = django.db.models.SlugField(
        verbose_name="слаг",
        max_length=150,
        unique=True,
        help_text="Максимальная длина - 150 символов",
    )

    class Meta:
        abstract = True


__all__ = []
