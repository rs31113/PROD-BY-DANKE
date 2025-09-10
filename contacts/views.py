from django.db.models import Prefetch
from django.views.generic import ListView

from contacts.models import LinkCategory, Link


class LinksView(ListView):
    model = LinkCategory
    template_name = "contacts/contacts.html"
    context_object_name = "categories"

    def get_queryset(self):
        return (
            LinkCategory.objects
            .order_by("order", "id")
            .prefetch_related(
                Prefetch(
                    "links",
                    queryset=Link.objects.filter(is_active=True).order_by("order", "id")
                )
            )
        )


__all__ = ()
