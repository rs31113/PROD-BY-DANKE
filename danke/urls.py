from django.contrib import admin
from django.shortcuts import render
from django.views.static import serve

from django.urls import include, path

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", include("main.urls", namespace="main")),
    path("shop/", include("shop.urls", namespace="shop")),
    path("gallery/", include("gallery.urls", namespace="gallery")),
    path("cart/", include("cart.urls", namespace="cart")),
    path("privacy/", include("privacy.urls", namespace="privacy")),
    path("terms/", include("terms.urls", namespace="terms")),
    path("contacts/", include("contacts.urls", namespace="contacts")),
    path("signup/", include("signup.urls", namespace="signup")),
    path("admin/", admin.site.urls),
    path("ckeditor5/", include("django_ckeditor_5.urls")),
]


def custom_404_view(request, exception):
    return render(request, "404.html", status=404)


handler404 = custom_404_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
    ]
