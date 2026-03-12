import os
import django
from django.db import connection

# configure django settings for tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.product_service.product_service.settings')
django.setup()

# create tables before any tests run
from services.product_service.catalog.infrastructure.models import Category, Product
with connection.schema_editor() as editor:
    # drop existing if any (to avoid conflicts between runs)
    try:
        editor.delete_model(Product)
    except Exception:
        pass
    try:
        editor.delete_model(Category)
    except Exception:
        pass
    # create base tables
    editor.create_model(Category)
    editor.create_model(Product)
