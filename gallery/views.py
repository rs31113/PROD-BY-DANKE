from django.views.generic import ListView
import gallery.models


class GalleryView(ListView):
    model = gallery.models.Photo
    template_name = "gallery/gallery.html"
    context_object_name = "photos"


__all__ = ()
