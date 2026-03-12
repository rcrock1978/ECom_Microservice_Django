import os
from celery import Celery

from shared.message_bus.bus import InMemoryMessageBus
from rewards.application.use_cases.expire_points import ExpirePointsUseCase
from rewards.infrastructure.processed_events import ProcessedEventStore
from rewards.infrastructure.repositories import InMemoryRewardRepository

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "reward_service.settings")
app = Celery("reward_service")
app.conf.broker_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
app.conf.result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")

REWARD_EXPIRATION_POINTS = int(os.getenv("REWARD_EXPIRATION_POINTS", "10"))
REWARD_EXPIRATION_INTERVAL_SECONDS = int(os.getenv("REWARD_EXPIRATION_INTERVAL_SECONDS", "2592000"))


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


@app.task(name="rewards.expire_points")
def expire_reward_points() -> int:
	repository = InMemoryRewardRepository()
	use_case = ExpirePointsUseCase(repository)
	return use_case.execute_scheduled(points=REWARD_EXPIRATION_POINTS, reason="scheduled-expiration")


app.conf.beat_schedule = {
	"rewards-expire-points": {
		"task": "rewards.expire_points",
		"schedule": REWARD_EXPIRATION_INTERVAL_SECONDS,
	}
}
