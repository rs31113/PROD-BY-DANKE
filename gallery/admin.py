from django.contrib import admin
from django.utils.html import format_html
import gallery.models


admin.site.site_title = "ADMIN"


@admin.register(gallery.models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "preview", "created_at")
    list_display_links = ("id", "title")
    search_fields = ("title",)
    list_filter = ("created_at",)
    date_hierarchy = "created_at"
    ordering = ("-created_at",)
    fields = ("title", "image", "created_at")
    list_per_page = 50

    @admin.display(description="Превью")
    def preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height:100px; border-radius:4px; object-fit:cover;" />',
                obj.image.url
            )
        return "—"


__all__ = ()
