from django.db import models


class OrderModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    order_number = models.CharField(max_length=32, unique=True)
    user_id = models.CharField(max_length=64)
    status = models.CharField(max_length=32, default="pending")
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    email = models.EmailField(null=True, blank=True)


class OrderItemModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    order_id = models.CharField(max_length=64)
    product_id = models.CharField(max_length=64)
    product_name = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
