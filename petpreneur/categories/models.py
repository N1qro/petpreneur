import django.core.exceptions
import django.db.models
import django.utils.text
import transliterate


import core.models


class Category(core.models.AbstractNameSlugModel):
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Subcategory(core.models.AbstractNameSlugModel):
    category = django.db.models.ForeignKey(
        Category,
        on_delete=django.db.models.CASCADE,
        verbose_name="категория",
        related_name="subcategory",
    )

    class Meta:
        verbose_name = "подкатегория"
        verbose_name_plural = "подкатегории"


class Skill(core.models.AbstractNameSlugModel):
    normalized_name = django.db.models.CharField(
        verbose_name="нормализованное имя навыка",
        max_length=150,
        help_text="нормализованное имя навыка",
        default="",
        editable=False,
    )

    class Meta:
        verbose_name = "навык"
        verbose_name_plural = "навыки"

    @staticmethod
    def normalize_name(name: str) -> str:
        return (
            django.utils.text.slugify(
                transliterate.translit(name, "ru", reversed=True),
            )
            .replace("-", "")
            .replace("_", "")
        )

    @classmethod
    def get_or_create(cls, name: str):
        normalized_name = cls.normalize_name(name)
        did_create = False

        try:
            skill = cls.objects.get(normalized_name=normalized_name)
        except cls.DoesNotExist:
            skill = cls.objects.create(
                name=name,
                normalized_name=normalized_name,
            )
            did_create = True

        return skill, did_create

    def clean(self):
        normalized_name = self.normalize_name(self.name)

        if Skill.objects.filter(normalized_name=normalized_name).exclude(
            id=self.id,
        ):
            raise django.core.exceptions.ValidationError(
                "Такой навык уже существует",
            )

        self.normalized_name = normalized_name

        super().clean()

    def save(self, *args, **kwargs):
        self.normalized_name = self.normalize_name(self.name)
        self.slug = self.normalized_name
        super().save(*args, **kwargs)


__all__ = []
