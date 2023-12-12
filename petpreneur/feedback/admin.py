import django.contrib.admin
import django.http

import feedback.models as fb_models


@django.contrib.admin.register(fb_models.Feedback)
class FeedbackAdmin(django.contrib.admin.ModelAdmin):
    list_display = (
        fb_models.Feedback.__str__,
        fb_models.Feedback.created_on.field.name,
        fb_models.Feedback.extra.field.name,
    )

    readonly_fields = (
        fb_models.Feedback.text.field.name,
        fb_models.Feedback.created_on.field.name,
        fb_models.Feedback.extra.field.name,
    )

    def has_add_permission(self, request: django.http.HttpRequest, obj=None):
        return False


@django.contrib.admin.register(fb_models.FeedbackExtra)
class FeedbackExtraAdmin(django.contrib.admin.ModelAdmin):
    readonly_fields = (
        fb_models.FeedbackExtra.mail.field.name,
        fb_models.FeedbackExtra.name.field.name,
    )

    def get_model_perms(self, request: django.http.HttpRequest):
        return {}

    def has_add_permission(self, request: django.http.HttpRequest, obj=None):
        return False

    def has_change_permission(
        self,
        request: django.http.HttpRequest,
        obj=None,
    ):
        return False


__all__ = []
