from django.db import models


class CartModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64, unique=True)
    coupon_code = models.CharField(max_length=50, null=True, blank=True)


class CartItemModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    cart_id = models.CharField(max_length=64)
    product_id = models.CharField(max_length=64)
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
