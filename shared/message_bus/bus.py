from .publisher import MessagePublisher
from .consumer import ConsumerRegistry, IdempotentConsumer, RetryPolicy
from .dlq import DeadLetterQueue


publisher = MessagePublisher()


class InMemoryMessageBus:
	def __init__(self, retry_policy: RetryPolicy | None = None) -> None:
		self.publisher = MessagePublisher()
		self.registry = ConsumerRegistry()
		self.idempotency = IdempotentConsumer()
		self.retry_policy = retry_policy or RetryPolicy()
		self.dlq = DeadLetterQueue()

	def register(self, routing_key: str, handler):
		self.registry.register(routing_key, handler)

	def publish_and_consume(self, event: object, routing_key: str) -> bool:
		self.publisher.publish(event=event, routing_key=routing_key)
		handler = self.registry.resolve(routing_key)
		if not handler:
			return True

		event_id = getattr(event, "event_id", "")

		processed_result = {"value": False}

		def handle_once() -> None:
			processed_result["value"] = self.idempotency.process(event_id=event_id, callback=lambda: handler(event))

		succeeded = self.retry_policy.run(handle_once)
		if not succeeded:
			self.dlq.push(event_id=event_id, reason=f"Failed processing routing key {routing_key}")
			return False
		return processed_result["value"]
