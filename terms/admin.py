from django.contrib import admin
import terms.models
import django.db.models
from django_ckeditor_5.widgets import CKEditor5Widget


class TermsAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.TextField: {"widget": CKEditor5Widget},
    }


admin.site.register(terms.models.Offer)


__all__ = ()
