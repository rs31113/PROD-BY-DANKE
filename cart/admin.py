from django.contrib import admin
import cart.models


admin.site.register(cart.models.Delivery)
admin.site.register(cart.models.Promocode)
admin.site.register(cart.models.Order)
admin.site.register(cart.models.CartItem)


__all__ = ()
