import core.models


class Resume(
    core.models.AbstractTextCreatedAtModel,
    core.models.AbstractIsActiveUserIdCategoryIdSubcategoryId,
):
    pass


__all__ = []
