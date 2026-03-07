import os
from django.core.wsgi import get_wsgi_application

from shared.common.logging_config import configure_logging
configure_logging()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'reward_service.settings')

application = get_wsgi_application()
