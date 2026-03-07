import os
import django
from django.core.management import call_command

# configure django settings for tests
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'services.auth_service.auth_service.settings')
django.setup()

# run migrations once before any tests
# because we want simple table creation, use schema_editor directly
from django.db import connection
from services.auth_service.auth_service.models import User, RefreshToken
with connection.schema_editor() as editor:
    # if tables already exist this will error; ignore by try/except
    try:
        editor.create_model(User)
    except Exception:
        pass
    try:
        editor.create_model(RefreshToken)
    except Exception:
        pass
