import os
from celery import Celery

from shared.message_bus.bus import InMemoryMessageBus
from rewards.infrastructure.processed_events import ProcessedEventStore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reward_service.settings")
app = Celery("reward_service")
app.conf.broker_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
app.conf.result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")


def register_consumers(bus: InMemoryMessageBus | None = None) -> InMemoryMessageBus:
	bus = bus or InMemoryMessageBus()
	processed_store = ProcessedEventStore()

	def handle_order_confirmed(event: object) -> None:
		event_id = getattr(event, "event_id")
		if processed_store.is_processed(event_id):
			return
		processed_store.mark_processed(event_id)

	bus.register("order.confirmed", handle_order_confirmed)
	return bus
