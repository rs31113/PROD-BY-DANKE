from django.views.generic.base import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from cart.models import CartItem, Delivery, Promocode, Order
from shop.models import Product, ProductSize, Size
import cart.forms
from django.contrib import messages
from django.utils import timezone
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


discount = 0


class AddToCart(View):
    def post(self, request, article):
        size = request.POST.get("size")
        quantity = request.POST.get("quantity")

        if not request.session.session_key:
            request.session.create()

        session_id = request.session.session_key

        product = get_object_or_404(Product, article=article)
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            size=size,
            session_id=session_id,
            quantity=quantity,
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        request.session.modified = True

        messages.success(request, f"Товар успешно добавлен в корзину!")

        return redirect("shop:product_detail", article=article)


class ViewCart(View):
    def get(self, request):
        session_id = request.session.session_key
        cart_items = CartItem.objects.filter(session_id=session_id)
        if cart_items.count() == 0:
            return render(request, "cart/empty_cart.html")
        deliveries = Delivery.objects.all()
        contact_info_form = cart.forms.ContactInfoForm()
        delivery_info_form = cart.forms.DeliveryInfoForm()
        promocode_form = cart.forms.PromocodeForm()
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        disable_increment = False

        for product in cart_items:
            item = Product.objects.get(id=product.product.id)
            size = product.size.strip()
            size = Size.objects.get(name=size)
            product_size = ProductSize.objects.get(product=item, size=size)
            if product_size.quantity == product.quantity:
                disable_increment = True

        context = {
            "cart_items": cart_items,
            "disable_increment": disable_increment,
            "deliveries": deliveries,
            "contact_info": contact_info_form,
            "delivery_info": delivery_info_form,
            "promocode_form": promocode_form,
            "total_price": total_price,
        }
        return render(request, "cart/cart.html", context)

    def post(self, request):
        action = request.POST["action"]
        global discount
        if action == "apply_promocode":
            promocode_form = cart.forms.PromocodeForm(request.POST)
            if promocode_form.is_valid():
                promocode = promocode_form.cleaned_data["code"]
                session_id = request.session.session_key
                cart_items = CartItem.objects.filter(session_id=session_id)
                deliveries = Delivery.objects.all()
                contact_info_form = cart.forms.ContactInfoForm()
                delivery_info_form = cart.forms.DeliveryInfoForm()
                total_price = sum(item.product.price * item.quantity for item in cart_items)
                context = {
                    "cart_items": cart_items,
                    "deliveries": deliveries,
                    "contact_info": contact_info_form,
                    "delivery_info": delivery_info_form,
                    "promocode_form": promocode_form,
                    "total_price": total_price,
                }
                try:
                    promocode_obj = Promocode.objects.get(name=promocode)
                    if promocode_obj.expiration_date > timezone.now().date():
                        discount = promocode_obj.value / 100
                        promocode_obj.limit -= 1
                        promocode_obj.save()
                        if promocode_obj.limit == 0:
                            promocode_obj.delete()
                        total_price = sum(item.product.price * item.quantity for item in cart_items)
                        total_price = total_price - int(total_price * discount)
                        promocode_response = f"Вы успешно применили промокод на {int(discount * 100)}%!"
                        context["total_price"] = total_price
                        context["promocode_response"] = promocode_response
                        return render(request, "cart/cart.html", context)
                    else:
                        promocode_obj.delete()
                        promocode_response = "Промокод не найден"
                        context["promocode_response"] = promocode_response
                        return render(request, "cart/cart.html", context)
                except Promocode.DoesNotExist:
                    promocode_response = "Промокод не найден"
                    context["promocode_response"] = promocode_response
                    return render(request, "cart/cart.html", context)

        elif action == "new_order":
            contact_info_form = cart.forms.ContactInfoForm(request.POST)
            delivery_info_form = cart.forms.DeliveryInfoForm(request.POST)
            delivery_id = request.POST.get("delivery")

            if contact_info_form.is_valid() and delivery_info_form.is_valid() and delivery_id:
                session_id = request.session.session_key
                cart_items = CartItem.objects.filter(session_id=session_id)
                total_price = sum(item.product.price * item.quantity for item in cart_items)
                total_price = total_price - int(total_price * discount)
                delivery_method = Delivery.objects.filter(id=delivery_id).first().name
                delivery_price = Delivery.objects.filter(id=delivery_id).first().price

                new_order = Order.objects.create(
                    contact_info=contact_info_form.cleaned_data,
                    delivery_info=delivery_info_form.cleaned_data,
                    total_price=total_price,
                    delivery_method=delivery_method,
                )

                for product in cart_items:
                    item = Product.objects.get(id=product.product.id)
                    new_order.products.add(item)
                    size = product.size.strip()
                    size = Size.objects.get(name=size)
                    product_size = ProductSize.objects.get(product=item, size=size)
                    product_size.quantity -= product.quantity

                    product_size.save()

                new_order.save()

                customer_name = request.POST.get("name")
                discount *= 100
                context = {
                    "order_id": new_order.id,
                    "name": customer_name,
                    "discount": discount,
                    "items": cart_items,
                    "total_price": total_price,
                    "amount": total_price + delivery_price,
                    "delivery_method": delivery_method,
                    "delivery_price": delivery_price,
                }
                discount = 0

                customer_email = request.POST.get("email")
                subject = "Подтверждение заказа"
                message = render_to_string("emails/order_confirmation_email.html", context)
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [customer_email]
                email = EmailMessage(
                    subject=subject,
                    body=message,
                    from_email=from_email,
                    to=recipient_list,
                )
                email.content_subtype = "html"
                cart_items.delete()
                email.send(fail_silently=True)

                return render(request, "cart/order_success.html", context)

            session_id = request.session.session_key
            cart_items = CartItem.objects.filter(session_id=session_id)
            deliveries = Delivery.objects.all()
            promocode_form = cart.forms.PromocodeForm()
            total_price = sum(item.product.price * item.quantity for item in cart_items)

            context = {
                "cart_items": cart_items,
                "deliveries": deliveries,
                "contact_info": contact_info_form,
                "delivery_info": delivery_info_form,
                "promocode_form": promocode_form,
                "total_price": total_price,
            }
            return render(request, "cart/cart.html", context)


class UpdateCart(View):
    def post(self, request, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
            session_id = request.session.session_key
            action = request.POST.get("action")
            if cart_item.quantity == 1 and action == "decrement":
                cart_item.delete()
                user_cart = CartItem.objects.filter(session_id=session_id)
                if not user_cart.exists():
                    return render(request, "cart/empty_cart.html")
            else:
                if action == "increment":
                    cart_item.quantity += 1
                else:
                    cart_item.quantity -= 1
                cart_item.save()
            return redirect("cart:cart")
        except CartItem.DoesNotExist:
            return redirect("cart:cart")


class DeleteItem(View):
    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        cart_item.delete()
        return redirect("cart:cart")


__all__ = ()
