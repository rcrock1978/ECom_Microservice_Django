from django.db import models


class CategoryModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    parent_id = models.CharField(max_length=64, null=True, blank=True)
    is_active = models.BooleanField(default=True)


class ProductModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category_id = models.CharField(max_length=64)
    image_url = models.URLField(null=True, blank=True)
    stock_quantity = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
