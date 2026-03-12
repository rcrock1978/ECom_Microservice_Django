from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RewardAccountModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("user_id", models.CharField(max_length=64, unique=True)),
                ("available_points", models.IntegerField(default=0)),
                ("lifetime_earned_points", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="RewardTransactionModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("user_id", models.CharField(max_length=64)),
                ("points", models.IntegerField()),
                ("transaction_type", models.CharField(max_length=32)),
                ("reason", models.CharField(max_length=120)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
