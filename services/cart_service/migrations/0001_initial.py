from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CartModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("user_id", models.CharField(max_length=64, unique=True)),
                ("coupon_code", models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CartItemModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("cart_id", models.CharField(max_length=64)),
                ("product_id", models.CharField(max_length=64)),
                ("product_name", models.CharField(max_length=255)),
                ("product_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.IntegerField(default=1)),
            ],
        ),
    ]
