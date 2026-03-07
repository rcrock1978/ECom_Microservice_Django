import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gateway.settings')
django.setup()
application = get_asgi_application()
