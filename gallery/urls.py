from django.urls import path
import gallery.views

app_name = "gallery"

urlpatterns = [
    path("", gallery.views.GalleryView.as_view(), name="gallery"),
]
