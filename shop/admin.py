import django.contrib
import django.db.models
import shop.models
from django_ckeditor_5.widgets import CKEditor5Widget


class ProductSizeInline(django.contrib.admin.TabularInline):
    model = shop.models.ProductSize


class ProductAdmin(django.contrib.admin.ModelAdmin):
    inlines = [ProductSizeInline]
    formfield_overrides = {
        django.db.models.TextField: {"widget": CKEditor5Widget},
    }


django.contrib.admin.site.register(shop.models.Product, ProductAdmin)
django.contrib.admin.site.register(shop.models.Size)
django.contrib.admin.site.register(shop.models.Photo)


__all__ = ()
