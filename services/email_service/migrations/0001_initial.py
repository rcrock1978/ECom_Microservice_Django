from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="EmailMessageModel",
            fields=[
                ("id", models.CharField(max_length=64, primary_key=True, serialize=False)),
                ("to_email", models.EmailField(max_length=254)),
                ("subject", models.CharField(max_length=255)),
                ("body_text", models.TextField()),
                ("body_html", models.TextField()),
                ("event_type", models.CharField(max_length=100)),
                ("status", models.CharField(default="pending", max_length=32)),
                ("retry_count", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        )
    ]
