from django.urls import path
import shop.views


app_name = "shop"

urlpatterns = [
    path("", shop.views.CatalogView.as_view(), name="catalog"),
    path(
        "<str:article>/",
        shop.views.ProductDetailView.as_view(),
        name="product_detail",
    ),
]


__all__ = ()
