import django.shortcuts


def home(request):
    template_name = "home/index.html"
    context = {}
    return django.shortcuts.render(request, template_name, context)


__all__ = []
