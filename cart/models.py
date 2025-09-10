from django.db import models
from shop.models import Product


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=1)
    session_id = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.quantity}"


class Delivery(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Delivery method"
        verbose_name_plural = "Delivery methods"


class Promocode(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.PositiveIntegerField(default=0)
    limit = models.PositiveIntegerField(default=1)
    expiration_date = models.DateField()


class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)
    contact_info = models.JSONField()
    delivery_info = models.JSONField()
    delivery_method = models.CharField(max_length=50)

    total_price = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order №{self.id}"


__all__ = ()
