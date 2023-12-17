import django.contrib

import resume.models


django.contrib.admin.site.register(resume.models.Resume)
