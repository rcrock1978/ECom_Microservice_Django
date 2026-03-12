from shared.message_bus.bus import InMemoryMessageBus
from shared.message_bus.consumer import RetryPolicy
from shared.message_bus.events import OrderConfirmedEvent


def test_publish_consume_idempotent_processing() -> None:
    bus = InMemoryMessageBus()
    processed: list[str] = []

    def handler(event: object) -> None:
        processed.append(getattr(event, "event_id"))

    bus.register("order.confirmed", handler)
    event = OrderConfirmedEvent.create(order_id="order-1", user_id="user-1", total=120.0)

    first = bus.publish_and_consume(event, routing_key="order.confirmed")
    second = bus.publish_and_consume(event, routing_key="order.confirmed")

    assert first is True
    assert second is False
    assert processed == [event.event_id]


def test_retry_then_success_processing() -> None:
    attempts = {"count": 0}
    bus = InMemoryMessageBus(retry_policy=RetryPolicy(max_retries=2))

    def flaky_handler(_: object) -> None:
        attempts["count"] += 1
        if attempts["count"] == 1:
            raise RuntimeError("transient")

    bus.register("order.confirmed", flaky_handler)
    event = OrderConfirmedEvent.create(order_id="order-2", user_id="user-2", total=80.0)

    result = bus.publish_and_consume(event, routing_key="order.confirmed")

    assert result is True
    assert attempts["count"] == 2
    assert len(bus.dlq.inspect()) == 0


def test_unrecoverable_message_goes_to_dlq() -> None:
    bus = InMemoryMessageBus(retry_policy=RetryPolicy(max_retries=1))

    def failing_handler(_: object) -> None:
        raise RuntimeError("boom")

    bus.register("order.confirmed", failing_handler)
    event = OrderConfirmedEvent.create(order_id="order-3", user_id="user-3", total=40.0)

    result = bus.publish_and_consume(event, routing_key="order.confirmed")

    assert result is False
    dlq_messages = bus.dlq.inspect()
    assert len(dlq_messages) == 1
    assert dlq_messages[0].event_id == event.event_id
