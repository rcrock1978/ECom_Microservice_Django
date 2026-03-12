import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "order_service.settings")
app = Celery("order_service")
app.conf.broker_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
app.conf.result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")
