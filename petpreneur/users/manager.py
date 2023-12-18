import django.contrib.auth.models

import jobs.models
import resume.models


class UserManager(django.contrib.auth.models.BaseUserManager):
    def get_jobs(self, user_id: int):
        user_resume = resume.models.Resume.objects.only(
            resume.models.Resume.id.field.name,
        ).get(user=user_id)
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


__all__ = []
