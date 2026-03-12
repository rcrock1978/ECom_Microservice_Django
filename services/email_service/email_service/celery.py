import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "email_service.settings")
app = Celery("email_service")
app.conf.broker_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
app.conf.result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")
