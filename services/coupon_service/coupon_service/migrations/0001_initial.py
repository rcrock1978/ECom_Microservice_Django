from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CouponModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("code", models.CharField(max_length=50, unique=True)),
                ("discount_type", models.CharField(max_length=20)),
                ("discount_value", models.DecimalField(decimal_places=2, max_digits=10)),
                ("min_order_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("max_discount_amount", models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ("usage_limit", models.IntegerField(blank=True, null=True)),
                ("used_count", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="CouponUsageModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("coupon_id", models.CharField(max_length=64)),
                ("user_id", models.CharField(max_length=64)),
            ],
        ),
    ]
