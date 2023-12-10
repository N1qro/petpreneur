import django.conf
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


class AbstractTextCreatedAtModel(django.db.models.Model):
    text = django.db.models.TextField(
        verbose_name="текст",
        help_text="Введите текст",
    )
    created_at = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата и время создания",
        help_text="Это поле создается автоматически",
    )

    class Meta:
        abstract = True


class AbstractIsActiveUserIdCategoryIdSubcategoryId(django.db.models.Model):
    is_active = django.db.models.BooleanField(
        default=True,
        verbose_name="активно",
        help_text="Поставьте галочку, если хотите сделать активным",
    )
    user = django.db.models.ForeignKey(
        django.conf.settings.AUTH_USER_MODEL,
        on_delete=django.db.models.CASCADE,
    )
    category = django.db.models.ForeignKey(
        to="categories.Category",
        on_delete=django.db.models.CASCADE,
    )
    subcategory = django.db.models.ForeignKey(
        to="categories.Subcategory",
        on_delete=django.db.models.CASCADE,
    )

    class Meta:
        abstract = True


__all__ = []
