import django.contrib

import categories.models


django.contrib.admin.site.register(
    categories.models.Category,
    prepopulated_fields={
        categories.models.Category.slug.field.name: (
            categories.models.Category.name.field.name,
        ),
    },
)

django.contrib.admin.site.register(
    categories.models.Subcategory,
    prepopulated_fields={
        categories.models.Subcategory.slug.field.name: (
            categories.models.Subcategory.name.field.name,
        ),
    },
)

django.contrib.admin.site.register(
    categories.models.Skill,
    prepopulated_fields={
        categories.models.Skill.slug.field.name: (
            categories.models.Skill.name.field.name,
        ),
    },
)

__all__ = []
