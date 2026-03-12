import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gateway.settings")
app = Celery("gateway")
app.conf.broker_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
app.conf.result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")
