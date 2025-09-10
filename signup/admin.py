from django.contrib import admin
import signup.models


@admin.register(signup.models.Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    ordering = ('-subscribed_at',)
    search_fields = ('email',)


__all__ = ()
