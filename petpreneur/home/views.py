import django.shortcuts
import django.views.generic


class HomeView(django.views.generic.TemplateView):
    template_name = "home/index.html"


__all__ = []
