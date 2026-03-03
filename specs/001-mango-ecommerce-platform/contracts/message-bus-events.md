# API Contracts: Message Bus Events

**Broker**: RabbitMQ 3.13+ with topic exchanges  
**Library**: Celery 5.x (publisher and consumer)

---

## Exchange Configuration

| Exchange | Type | Durable | Description |
|----------|------|---------|-------------|
| `mango.events` | topic | yes | All domain events across services |
| `mango.dlx` | direct | yes | Dead-letter exchange for failed messages |

## Routing Key Pattern

Format: `{service}.{entity}.{action}`

| Routing Key | Publisher | Description |
|-------------|----------|-------------|
| `auth.user.registered` | Auth | New user account created |
| `auth.user.password_reset_requested` | Auth | Password reset initiated |
| `order.order.confirmed` | Order | Payment successful, order confirmed |
| `order.order.status_changed` | Order | Order status transition |
| `order.payment.completed` | Order | Payment intent fulfilled |
| `order.payment.failed` | Order | Payment failed |
| `product.inventory.low_stock` | Product | Stock below threshold |
| `reward.points.earned` | Reward | Points credited to account |

## Queue Bindings

| Queue | Binding Key | Consumer | Purpose |
|-------|------------|----------|---------|
| `email.user_events` | `auth.user.*` | Email | Registration, password reset emails |
| `email.order_events` | `order.order.*` | Email | Order confirmation, status update emails |
| `email.payment_events` | `order.payment.failed` | Email | Payment failure notification |
| `email.reward_events` | `reward.points.earned` | Email | Reward milestone notification |
| `reward.order_events` | `order.order.confirmed` | Reward | Credit points on order confirmation |
| `product.order_events` | `order.order.confirmed` | Product | Decrement inventory on order confirmation |
| `product.order_cancel` | `order.order.status_changed` | Product | Restore inventory on cancellation |

## Message Envelope

All events use this standard envelope:

```json
{
  "event_id": "uuid-v4",
  "event_type": "auth.user.registered",
  "timestamp": "2026-03-04T14:30:00Z",
  "version": "1.0",
  "source": "auth-service",
  "correlation_id": "uuid-v4-from-original-request",
  "payload": {
    // Event-specific data
  }
}
```

## Delivery Guarantees

- **Publisher**: Confirm mode enabled (RabbitMQ publisher confirms)
- **Consumer**: Manual acknowledgment after successful processing
- **Retry**: Failed messages retried 3 times with exponential backoff (via Celery `autoretry_for`)
- **Dead-Letter**: After max retries, routed to `mango.dlx` → `{service}.dlq` queue
- **Idempotency**: Every consumer checks `event_id` to prevent duplicate processing
- **Message TTL**: 7 days in dead-letter queue; alerts trigger for unprocessed DLQ messages
- **Ordering**: Not guaranteed; consumers must handle out-of-order delivery

## Consumer Idempotency Pattern

Each consumer service maintains a `ProcessedEvent` table:

```json
{
  "event_id": "uuid",
  "event_type": "order.order.confirmed",
  "processed_at": "2026-03-04T14:30:05Z"
}
```

Before processing, check if `event_id` exists. If yes, acknowledge and skip. This ensures at-least-once delivery does not cause duplicate side effects.
