from django.shortcuts import get_object_or_404
import django.views
import terms.models


class TermsView(django.views.generic.TemplateView):
    model = terms.models.Offer
    template_name = "terms/terms.html"
    context_object_name = "offer"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        offer = get_object_or_404(terms.models.Offer, name="public offer")
        context[self.context_object_name] = offer
        return context


__all__ = ()
