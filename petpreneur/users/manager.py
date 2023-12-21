import django.contrib.auth.models
from django.utils.translation import gettext_lazy as _

import jobs.models
import resume.models


class UserManager(django.contrib.auth.models.BaseUserManager):
    def get_jobs(self, user):
        user_resume = resume.models.Resume.objects.only(
            resume.models.Resume.id.field.name,
        ).get(user=user)
        return jobs.models.JobRequests.objects.select_related(
            jobs.models.JobRequests.job.field.name,
        ).filter(resume=user_resume)

    def get_current_jobs(self, user_id):
        return (
            self.get_jobs(user_id=user_id)
            .filter(status=2)
            .only(
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.title.field.name}",
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.image.field.name}",
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.created_at.field.name}",
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.text.field.name}",
            )
        )

    def get_request_jobs(self, user_id):
        return (
            self.get_jobs(user_id=user_id)
            .filter(status=1)
            .only(
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.title.field.name}",
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.image.field.name}",
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.created_at.field.name}",
                f"{jobs.models.JobRequests.job.field.name}"
                f"__{jobs.models.Job.text.field.name}",
            )
        )

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_("The Email must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        resume.models.Resume.objects.create(
            user=user,
        )
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True."))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        return self.create_user(email, password, **extra_fields)


__all__ = []
