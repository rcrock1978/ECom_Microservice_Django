from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('hashed_password', models.CharField(max_length=256)),
                ('role', models.CharField(choices=[('customer', 'customer'), ('admin', 'admin')], default='customer', max_length=20)),
                ('is_locked', models.BooleanField(default=False)),
                ('failed_attempts', models.IntegerField(default=0)),
                ('is_verified', models.BooleanField(default=False)),
                ('verification_token', models.CharField(blank=True, max_length=64, null=True)),
                ('token_expiry', models.DateTimeField(blank=True, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='RefreshToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=128, unique=True)),
                ('expires_at', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_service.User')),
            ],
        ),
    ]
