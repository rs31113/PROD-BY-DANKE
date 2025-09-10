from django.contrib import admin
import contacts.models


class LinkInline(admin.TabularInline):
    model = contacts.models.Link
    extra = 1
    fields = ("label", "url", "order", "is_active")


@admin.register(contacts.models.LinkCategory)
class LinkCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "order")
    list_editable = ("order",)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("order", "id")
    inlines = [LinkInline]


@admin.register(contacts.models.Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ("label", "category", "order", "is_active")
    list_editable = ("order", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("label", "url")
    ordering = ("category__order", "order", "id")


__app__ = ()
