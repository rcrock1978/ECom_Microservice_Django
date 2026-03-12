import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','services.product_service.product_service.settings')
import django

django.setup()
from django.apps import apps
print([(app.name, app.label) for app in apps.get_app_configs() if 'catalog' in app.name or 'catalog' in app.label])
