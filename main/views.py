import django.views


class MainView(django.views.generic.TemplateView):
    template_name = "main.html"


__all__ = ()
