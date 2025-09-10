from django.contrib import admin
import privacy.models
import django.db.models
from django_ckeditor_5.widgets import CKEditor5Widget


class PrivacyAdmin(admin.ModelAdmin):
    formfield_overrides = {
        django.db.models.TextField: {"widget": CKEditor5Widget},
    }


admin.site.register(privacy.models.Offer)


__all__ = ()
