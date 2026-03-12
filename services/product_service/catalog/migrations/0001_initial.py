from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="CategoryModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("parent_id", models.CharField(blank=True, max_length=64, null=True)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name="ProductModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("slug", models.SlugField(unique=True)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                ("category_id", models.CharField(max_length=64)),
                ("image_url", models.URLField(blank=True, null=True)),
                ("stock_quantity", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
            ],
        ),
    ]
