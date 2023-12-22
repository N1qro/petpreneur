import django.contrib.auth
import django.contrib.auth.backends
import django.utils.timezone

import resume.models
import users.models


class EmailOrUsernameModelBackend(django.contrib.auth.backends.ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(users.models.User.USERNAME_FIELD)
        if username is None or password is None:
            return None
        try:
            if "@" in username:
                user = users.models.User.objects.by_mail(username)
            else:
                user = users.models.User.objects.get(username=username)
        except users.models.User.DoesNotExist:
            users.models.User().set_password(password)
        else:
            if not hasattr(user, "resume"):
                resume.models.Resume.objects.create(
                    user=user,
                )
            if user.check_password(password):
                return user


__all__ = []
