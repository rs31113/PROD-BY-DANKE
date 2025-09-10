from django.shortcuts import get_object_or_404
import django.views
import shop.models
import cart.models


def get_quantity_in_cart(request, product, size):
    session_id = request.session.session_key
    cart_item = cart.models.CartItem.objects.filter(product=product, session_id=session_id)
    for item in cart_item:
        if size.strip() == item.size.strip():
            return item.quantity
    return 0


class CatalogView(django.views.generic.ListView):
    model = shop.models.Product
    template_name = "shop/catalog.html"
    context_object_name = "catalog"


class ProductDetailView(django.views.generic.DetailView):
    model = shop.models.Product
    template_name = "shop/product_detail.html"
    context_object_name = "product"

    def get_object(self, queryset=None):
        article = self.kwargs["article"]
        return get_object_or_404(shop.models.Product, article=article)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = context[self.context_object_name]

        available_sizes = dict()
        all_disabled = list()

        for product_size in shop.models.ProductSize.objects.filter(product=product):
            cart_quantity = get_quantity_in_cart(self.request, product, product_size.size.name)
            quantity = product_size.quantity - cart_quantity
            disabled = (quantity == 0)
            available_sizes[product_size.size.name] = {
                "quantity": quantity,
                "disabled": disabled,
            }
            all_disabled.append(disabled)

        all_disabled = all(elem is True for elem in all_disabled)

        context["all_disabled"] = all_disabled
        context["available_sizes"] = available_sizes

        return context


__all__ = ()
