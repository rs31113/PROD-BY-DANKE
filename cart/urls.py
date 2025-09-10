from django.urls import path
import cart.views


app_name = "cart"

urlpatterns = [
    path("", cart.views.ViewCart.as_view(), name="cart"),
    path("add/<str:article>/", cart.views.AddToCart.as_view(), name="add_item"),
    path("update/<int:cart_item_id>/", cart.views.UpdateCart.as_view(), name="update_cart"),
    path("delete/<int:cart_item_id>/", cart.views.DeleteItem.as_view(), name="delete_item"),
]
