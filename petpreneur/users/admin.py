import django.contrib

import users.models


django.contrib.admin.site.register(users.models.User)
