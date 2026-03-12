from django.db import models


class CouponModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20)
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    min_order_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    max_discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usage_limit = models.IntegerField(null=True, blank=True)
    used_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)


class CouponUsageModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    coupon_id = models.CharField(max_length=64)
    user_id = models.CharField(max_length=64)
