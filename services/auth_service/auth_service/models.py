from django.db import models


class UserModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    role = models.CharField(max_length=20, default="customer")
    failed_login_attempts = models.IntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)


class RefreshTokenModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64)
    token_hash = models.CharField(max_length=255, unique=True)
    is_blacklisted = models.BooleanField(default=False)
