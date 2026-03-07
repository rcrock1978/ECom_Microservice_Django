from django.db import models
from django.utils import timezone


class UserRole(models.TextChoices):
    CUSTOMER = 'customer', 'customer'
    ADMIN = 'admin', 'admin'


class User(models.Model):
    email = models.EmailField(unique=True)
    hashed_password = models.CharField(max_length=256)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CUSTOMER)
    is_locked = models.BooleanField(default=False)
    failed_attempts = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email


class RefreshToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=128, unique=True)
    expires_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() >= self.expires_at
