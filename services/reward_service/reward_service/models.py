from django.db import models


class RewardAccountModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64, unique=True)
    available_points = models.IntegerField(default=0)
    lifetime_earned_points = models.IntegerField(default=0)


class RewardTransactionModel(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    user_id = models.CharField(max_length=64)
    points = models.IntegerField()
    transaction_type = models.CharField(max_length=32)
    reason = models.CharField(max_length=120)
    created_at = models.DateTimeField(auto_now_add=True)
