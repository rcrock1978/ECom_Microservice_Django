from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OrderModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("order_number", models.CharField(max_length=32, unique=True)),
                ("user_id", models.CharField(max_length=64)),
                ("status", models.CharField(default="pending", max_length=32)),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=10)),
                ("discount_amount", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("total_amount", models.DecimalField(decimal_places=2, max_digits=10)),
                ("email", models.EmailField(blank=True, max_length=254, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="OrderItemModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("order_id", models.CharField(max_length=64)),
                ("product_id", models.CharField(max_length=64)),
                ("product_name", models.CharField(max_length=255)),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("quantity", models.IntegerField(default=1)),
            ],
        ),
    ]
