from cart.models import CartItem


def cart_items_count(request):
    session_id = request.session.session_key
    cart_items = CartItem.objects.filter(session_id=session_id)
    cart_items_count = cart_items.count()
    return {"cart_items_count": cart_items_count}


__all__ = ()
