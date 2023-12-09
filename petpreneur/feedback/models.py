import django.conf
import django.db.models


class FeedbackExtra(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=254,
        verbose_name="имя",
        blank=True,
    )
    mail = django.db.models.EmailField(
        verbose_name="почта",
    )

    class Meta:
        verbose_name = "данные к обращению"
        verbose_name_plural = "данные к обращениям"

    def __str__(self):
        return self.mail


class Feedback(django.db.models.Model):
    text = django.db.models.TextField(
        verbose_name="текст",
    )
    created_on = django.db.models.DateTimeField(
        auto_now_add=True,
        verbose_name="дата и время создания",
        null=True,
    )

    extra = django.db.models.OneToOneField(
        FeedbackExtra,
        on_delete=django.db.models.CASCADE,
        related_name="feedbackExtra",
        related_query_name="FeedbackExtra",
        verbose_name="доп. данные",
    )

    class Meta:
        verbose_name = "обращение"
        verbose_name_plural = "обращения"

    def __str__(self):
        if len(str(self.text)) > 20:
            return self.text[:20] + "..."
        return self.text[:20]


__all__ = []
