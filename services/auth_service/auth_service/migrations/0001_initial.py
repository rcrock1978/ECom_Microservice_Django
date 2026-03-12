from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UserModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=150)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password_hash", models.CharField(max_length=255)),
                ("role", models.CharField(default="customer", max_length=20)),
                ("failed_login_attempts", models.IntegerField(default=0)),
                ("locked_until", models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="RefreshTokenModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("user_id", models.CharField(max_length=64)),
                ("token_hash", models.CharField(max_length=255, unique=True)),
                ("is_blacklisted", models.BooleanField(default=False)),
            ],
        ),
    ]
