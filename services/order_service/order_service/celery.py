import os
from celery import Celery

from orders.application.use_cases.handle_order_timeout import HandleOrderTimeoutUseCase
from orders.infrastructure.repositories import InMemoryOrderRepository

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "order_service.settings")
app = Celery("order_service")
app.conf.broker_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")
app.conf.result_backend = os.getenv("REDIS_URL", "redis://localhost:6379/0")

TIMEOUT_MINUTES = int(os.getenv("ORDER_TIMEOUT_MINUTES", "15"))


@app.task(name="orders.monitor_pending_timeouts")
def monitor_pending_order_timeout(order_number: str) -> str:
	repository = InMemoryOrderRepository()
	use_case = HandleOrderTimeoutUseCase(repository)
	order = use_case.execute(order_number=order_number)
	return order.status


app.conf.beat_schedule = {
	"orders-monitor-timeouts": {
		"task": "orders.monitor_pending_timeouts",
		"schedule": TIMEOUT_MINUTES * 60,
	}
}
