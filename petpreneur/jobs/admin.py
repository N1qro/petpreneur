import django.contrib

import jobs.models


django.contrib.admin.site.register(jobs.models.Job)
django.contrib.admin.site.register(jobs.models.JobRequests)
